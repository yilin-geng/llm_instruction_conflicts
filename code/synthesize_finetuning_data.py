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
from priority_control_policies import *

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

# Initialize policies
policies = [
    ConstraintFollowingBaseline("constraint_following_baseline"),
    BaselineAllUserPolicy("baseline_all_user"),
    BasicSeparationPolicy("basic_separation"),
    TaskSpecifiedSeparationPolicy("task_specified_separation"), 
    EmphasizedSeparationPolicy("emphasized_separation"),
    # UnmarkedSystemPolicyBasic("unmarked_system_basic"),
    # MarkedSystemPolicyBasic("marked_system_basic"),
    # UnmarkedUserPolicyBasic("unmarked_user_basic"),
    # MarkedUserPolicyBasic("marked_user_basic"),
    # UnmarkedSystemPolicyDetailed("unmarked_system_detailed"),
    # MarkedSystemPolicyDetailed("marked_system_detailed"),
    # UnmarkedUserPolicyDetailed("unmarked_user_detailed"),
    # MarkedUserPolicyDetailed("marked_user_detailed"),
]


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

def load_responses(finetuning_data_without_ideal_output: List[Dict], output_file: Path) -> List[Dict]:
    with open(output_file, 'r') as f:
        data = [json.loads(line) for line in f]
    if len(data) != len(finetuning_data_without_ideal_output):
        raise ValueError(f"Length of data in {output_file} does not match length of finetuning_data_without_ideal_output")
    for d1, d2 in zip(data, finetuning_data_without_ideal_output):
        if d1["base_instruction"] != d2["base_instruction"]:
            raise ValueError(f"Base instruction mismatch between {output_file} and finetuning_data_without_ideal_output")
        d2["ideal_output"] = d1["ideal_output"]

def augment_with_policies(finetuning_data_with_ideal_output: List[Dict]) -> List[Dict]:
    finetuning_data_with_policies = []
    for data in finetuning_data_with_ideal_output:
        for policy in policies:
            finetuning_datapoint = data.copy()
            system_prompt, user_prompt = policy.get_prompts(
                data["base_instruction"], 
                data["constraint1"], 
                data["constraint2"])

            message = []
            if system_prompt:
                message.append({"role": "system", "content": system_prompt})
            message.append({"role": "user", "content": user_prompt})
            finetuning_datapoint["input_message"] = message
            finetuning_data_with_policies.append(finetuning_datapoint)
    return finetuning_data_with_policies

async def process_dataset_with_policies(
    data_list: List[Dict],
    output_file: Path,
    output_file_with_policies: Path,
    is_reversed: bool,
    dataset_name: str
) -> None:
    """Process a dataset and generate its policy-augmented version."""
    if not output_file.exists():
        logger.info(f"Generating ideal outputs for {dataset_name}...")
        await process_data_batch(data_list, is_reversed=is_reversed)
        save_conflicting_data(data_list, output_file)
    else:
        logger.info(f"Skipping {dataset_name} generation as file already exists: {output_file}")
    
    load_responses(data_list, output_file)
    data_with_policies = augment_with_policies(data_list)
    save_conflicting_data(data_with_policies, output_file_with_policies)

async def main_async():
    output_index = 1
    base_instructions_file = root_dir / 'data' / 'base_instructions_picked.csv'
    output_file_training_normal = root_dir / 'data' / 'finetuning_data' / f'finetuning_data_training_normal_{output_index}.jsonl'
    output_file_training_reversed = root_dir / 'data' / 'finetuning_data' / f'finetuning_data_training_reversed_{output_index}.jsonl'
    output_file_test_normal = root_dir / 'data' / 'finetuning_data' / f'finetuning_data_test_normal_{output_index}.jsonl'
    output_file_test_reversed = root_dir / 'data' / 'finetuning_data' / f'finetuning_data_test_reversed_{output_index}.jsonl'
    
    output_file_training_normal_with_policies = root_dir / 'data' / 'finetuning_data' / f'finetuning_data_training_normal_with_policies_{output_index}.jsonl'
    output_file_training_reversed_with_policies = root_dir / 'data' / 'finetuning_data' / f'finetuning_data_training_reversed_with_policies_{output_index}.jsonl'
    output_file_test_normal_with_policies = root_dir / 'data' / 'finetuning_data' / f'finetuning_data_test_normal_with_policies_{output_index}.jsonl'
    output_file_test_reversed_with_policies = root_dir / 'data' / 'finetuning_data' / f'finetuning_data_test_reversed_with_policies_{output_index}.jsonl'
    
    logger.info("Generating conflicting instructions...")
    if not base_instructions_file.exists():
        logger.error(f"Input file not found: {base_instructions_file}")
        return

    test_conflict_names = [
        [
            "num_sentence_conflict: 12_7",
            "keyword_frequency_conflict: often_6_3"
        ],
        [
            "language_conflict: it_es",
            "case_conflict"
        ],
        [
            "word_length_conflict: 100_30",
            "keyword_forbidden_conflict: many_special"
        ]
    ]

        
    # Generate normal conflicting data
    conflicting_data_normal = generate_conflicting_data(
        base_instructions_file, 
        flip_instructions=False, 
        conflict_dict=INSTRUCTION_CONFLICTS_FOR_FINETUNING
    )
    
    # Split normal data into training and test
    finetuning_data_training_normal = [
        data for data in conflicting_data_normal 
        if data["conflict_name"] not in test_conflict_names[output_index]
    ]
    finetuning_data_test_normal = [
        data for data in conflicting_data_normal 
        if data["conflict_name"] in test_conflict_names[output_index]
    ]
    
    conflicting_data_reversed = generate_conflicting_data(
        base_instructions_file, 
        flip_instructions=True, 
        conflict_dict=INSTRUCTION_CONFLICTS_FOR_FINETUNING
    )
    
    # Split reversed data into training and test
    finetuning_data_training_reversed = [
        data for data in conflicting_data_reversed 
        if data["conflict_name"] not in test_conflict_names[output_index]
    ]
    finetuning_data_test_reversed = [
        data for data in conflicting_data_reversed 
        if data["conflict_name"] in test_conflict_names[output_index]
    ]

    logger.info(f"Generated {len(finetuning_data_training_normal)} normal training, "
                f"{len(finetuning_data_test_normal)} normal test, "
                f"{len(finetuning_data_training_reversed)} reversed training, "
                f"{len(finetuning_data_test_reversed)} reversed test data")

    # Process all datasets
    datasets = [
        (finetuning_data_test_normal, output_file_test_normal, output_file_test_normal_with_policies, False, "normal test data"),
        (finetuning_data_test_reversed, output_file_test_reversed, output_file_test_reversed_with_policies, True, "reversed test data"),
        (finetuning_data_training_normal, output_file_training_normal, output_file_training_normal_with_policies, False, "normal training data"),
        (finetuning_data_training_reversed, output_file_training_reversed, output_file_training_reversed_with_policies, True, "reversed training data")
    ]

    for data_list, output_file, output_file_with_policies, is_reversed, dataset_name in datasets:
        await process_dataset_with_policies(
            data_list,
            output_file,
            output_file_with_policies,
            is_reversed,
            dataset_name
        )

    logger.info(f"Final dataset sizes - \n"
                f"Normal Training: {len(finetuning_data_training_normal)}, \n"
                f"Normal Test: {len(finetuning_data_test_normal)}, \n"
                f"Reversed Training: {len(finetuning_data_training_reversed)}, \n"
                f"Reversed Test: {len(finetuning_data_test_reversed)}")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
