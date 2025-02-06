import json
import logging
from pathlib import Path
from typing import Dict, List
import pandas as pd
from tqdm import tqdm
import asyncio
from tqdm.asyncio import tqdm_asyncio
import time

root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from conflicts_dict import INSTRUCTION_CONFLICTS_FOR_FINETUNING
from synthesize_conflicting_data import generate_conflicting_data, save_conflicting_data
from llm_api import get_completion_gpt4o_async
from priority_control_policies import BaselineAllUserPolicy, BasicSeparationPolicy

class RateLimiter:
    def __init__(self, max_requests_per_minute: int):
        self.max_requests = max_requests_per_minute
        self.window_size = 60  # 60 seconds = 1 minute
        self.requests = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        async with self.lock:
            current_time = time.time()
            # Remove requests older than window_size
            self.requests = [t for t in self.requests if current_time - t < self.window_size]
            
            if len(self.requests) >= self.max_requests:
                # Wait until the oldest request expires
                wait_time = self.window_size - (current_time - self.requests[0])
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
                self.requests = self.requests[1:]
            
            self.requests.append(current_time)

# Create global rate limiter and semaphore
RATE_LIMITER = RateLimiter(max_requests_per_minute=20)
MAX_CONCURRENT_REQUESTS = 20
SEMAPHORE = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

async def generate_ideal_output(data: Dict, is_reversed: bool = False) -> tuple[str, list[dict]]:
    """Generate ideal output and input message for a given instruction using GPT-4."""
    policy = BaselineAllUserPolicy("baseline_all_user")
    
    # # Create BasicSeparationPolicy for input message format
    # separation_policy = BasicSeparationPolicy("basic_separation")
    # system_prompt, user_prompt = separation_policy.get_prompts(
    #     data['base_instruction'], 
    #     data['constraint1'], 
    #     data['constraint2']
    # )
    
    system_prompt = "You are generating responses that fulfill the following constraints: " + data['constraint1']
    user_prompt = data['base_instruction'] + 'You MUST fulfill the following constraint for your response: ' + data['constraint1']

    # Create input message in API format
    input_message = []
    if system_prompt:
        input_message.append({"role": "system", "content": system_prompt})
    input_message.append({"role": "user", "content": user_prompt})
    
    # Try up to 3 times to get a valid response
    for _ in range(3):
        try:
            async with SEMAPHORE:  # Limit concurrent requests
                await RATE_LIMITER.acquire()  # Rate limit requests
                response = await get_completion_gpt4o_async(
                    system_prompt=system_prompt,
                    messages=user_prompt
                )
            # Evaluate if response meets primary constraint
            evaluation = policy.evaluate_responses([data], [response], is_reversed=is_reversed, conflicts_dict=INSTRUCTION_CONFLICTS_FOR_FINETUNING)[0]
            if evaluation.primary_constraint_met > 0.5:
                return response, input_message
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            await asyncio.sleep(1)  # Wait a bit before retrying
    
    logger.warning(f"Failed to generate valid response for {data['base_instruction']}\n"
                    f"Prompt: {user_prompt}\n"
                    f"Response: {response}")
    return "", input_message

async def process_data_batch(data_list: List[Dict], is_reversed: bool = False) -> None:
    """Process a batch of data in parallel using asyncio.gather"""
    tasks = []
    for data in data_list:
        tasks.append(generate_ideal_output(data, is_reversed))
    
    results = await tqdm_asyncio.gather(*tasks)
    
    for data, (ideal_output, input_message) in zip(data_list, results):
        data["ideal_output"] = ideal_output
        data["input_message"] = input_message

async def main_async():
    base_instructions_file = root_dir / 'data' / 'base_instructions_picked.csv'
    output_file_training_normal = root_dir / 'data' / 'finetuning_data' / 'finetuning_data_training_normal.jsonl'
    output_file_test_normal = root_dir / 'data' / 'finetuning_data' / 'finetuning_data_test_normal.jsonl'
    output_file_training_reversed = root_dir / 'data' / 'finetuning_data' / 'finetuning_data_training_reversed.jsonl'
    output_file_test_reversed = root_dir / 'data' / 'finetuning_data' / 'finetuning_data_test_reversed.jsonl'
    
    logger.info("Generating conflicting instructions...")
    if not base_instructions_file.exists():
        logger.error(f"Input file not found: {base_instructions_file}")
        return
        
    # Generate normal conflicting data
    conflicting_data_normal = generate_conflicting_data(
        base_instructions_file, 
        flip_instructions=False, 
        conflict_dict=INSTRUCTION_CONFLICTS_FOR_FINETUNING
    )
    
    # Split normal data into training and test
    finetuning_data_training_normal = [
        data for data in conflicting_data_normal 
        # if data["conflict_name"] not in ["num_sentence_conflict: 12_7", "keyword_frequency_conflict: often_6_3"]
    ]
    finetuning_data_test_normal = [
        data for data in conflicting_data_normal 
        # if data["conflict_name"] in ["num_sentence_conflict: 12_7", "keyword_frequency_conflict: often_6_3"]
    ]
    
    conflicting_data_reversed = generate_conflicting_data(
        base_instructions_file, 
        flip_instructions=True, 
        conflict_dict=INSTRUCTION_CONFLICTS_FOR_FINETUNING
    )
    
    # Split reversed data into training and test
    finetuning_data_training_reversed = [
        data for data in conflicting_data_reversed 
        if data["conflict_name"] not in ["num_sentence_conflict: 12_7", "keyword_frequency_conflict: often_6_3"]
    ]
    finetuning_data_test_reversed = [
        data for data in conflicting_data_reversed 
        if data["conflict_name"] in ["num_sentence_conflict: 12_7", "keyword_frequency_conflict: often_6_3"]
    ]

    logger.info(f"Generated {len(finetuning_data_training_normal)} normal training, "
                f"{len(finetuning_data_test_normal)} normal test, "
                f"{len(finetuning_data_training_reversed)} reversed training, "
                f"{len(finetuning_data_test_reversed)} reversed test data")

    logger.info("Generating ideal outputs for normal test data...")
    await process_data_batch(finetuning_data_test_normal, is_reversed=False)
    save_conflicting_data(finetuning_data_test_normal, output_file_test_normal)
    
    logger.info("Generating ideal outputs for reversed test data...")
    await process_data_batch(finetuning_data_test_reversed, is_reversed=True)
    save_conflicting_data(finetuning_data_test_reversed, output_file_test_reversed)

    # Generate ideal outputs for all datasets in parallel
    logger.info("Generating ideal outputs for normal training data...")
    await process_data_batch(finetuning_data_training_normal, is_reversed=False)
    save_conflicting_data(finetuning_data_training_normal, output_file_training_normal)
    
    logger.info("Generating ideal outputs for reversed training data...")
    await process_data_batch(finetuning_data_training_reversed, is_reversed=True)
    save_conflicting_data(finetuning_data_training_reversed, output_file_training_reversed)
    
    logger.info(f"Final dataset sizes - \n"
                f"Normal Training: {len(finetuning_data_training_normal)}, \n"
                f"Normal Test: {len(finetuning_data_test_normal)}, \n"
                f"Reversed Training: {len(finetuning_data_training_reversed)}, \n"
                f"Reversed Test: {len(finetuning_data_test_reversed)}")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
