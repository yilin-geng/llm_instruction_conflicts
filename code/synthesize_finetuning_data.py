import json
import logging
from pathlib import Path
from typing import Dict, List
import pandas as pd
from tqdm import tqdm

root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from conflicts_dict import INSTRUCTION_CONFLICTS_FOR_FINETUNING
from synthesize_conflicting_data import generate_conflicting_data, save_conflicting_data
from llm_api import get_completion_gpt4o
from priority_control_policies import BaselineAllUserPolicy, BasicSeparationPolicy

def generate_ideal_output(data: Dict, is_reversed: bool = False) -> tuple[str, list[dict]]:
    """Generate ideal output and input message for a given instruction using GPT-4."""
    policy = BaselineAllUserPolicy("baseline_all_user")
    
    # Create BasicSeparationPolicy for input message format
    separation_policy = BasicSeparationPolicy("basic_separation")
    system_prompt, user_prompt = separation_policy.get_prompts(
        data['base_instruction'], 
        data['constraint1'], 
        data['constraint2']
    )
    
    # Create input message in API format
    input_message = []
    if system_prompt:
        input_message.append({"role": "system", "content": system_prompt})
    input_message.append({"role": "user", "content": user_prompt})
    
    # Prepare single prompt for generating output
    # data["constraint2"] = ""
    # conflict_data = [data]
    # conflict_data, prompts = policy.prepare_evaluation_batch(conflict_data)
    # _, user_prompt = prompts[0]


    # user_prompt = f'{base_instruction}{contraint1}'
    system_prompt = "You are generating responses that fulfill the following constraints: " + data['constraint1']
    user_prompt = data['base_instruction'] + 'You MUST fulfill the following constraint for your response: ' + data['constraint1']
    
    
    # Try up to 3 times to get a valid response
    for _ in range(3):
        response = get_completion_gpt4o(
            system_prompt=system_prompt,
            messages=user_prompt
        )
        # Evaluate if response meets primary constraint
        evaluation = policy.evaluate_responses([data], [response], is_reversed=is_reversed, conflicts_dict=INSTRUCTION_CONFLICTS_FOR_FINETUNING)[0]
        if evaluation.primary_constraint_met > 0.5:
            return response, input_message
    
    logger.warning(f"Failed to generate valid response for {data['base_instruction']}\n"
                    f"Prompt: {user_prompt}\n"
                    f"Response: {response}")
    return "", input_message

def main():
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
        if data["conflict_name"] not in ["num_sentence_conflict: 12_7", "keyword_frequency_conflict: often_6_3"]
    ]
    finetuning_data_test_normal = [
        data for data in conflicting_data_normal 
        if data["conflict_name"] in ["num_sentence_conflict: 12_7", "keyword_frequency_conflict: often_6_3"]
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

    # # Generate ideal outputs for normal data
    # logger.info("Generating ideal outputs for normal training data...")
    # for data in tqdm(finetuning_data_training_normal):
    #     ideal_output, input_message = generate_ideal_output(data, is_reversed=False)
    #     data["ideal_output"] = ideal_output
    #     data["input_message"] = input_message

    # save_conflicting_data(finetuning_data_training_normal, output_file_training_normal)
    
    # logger.info("Generating ideal outputs for normal test data...")
    # for data in tqdm(finetuning_data_test_normal):
    #     ideal_output, input_message = generate_ideal_output(data, is_reversed=False)
    #     data["ideal_output"] = ideal_output
    #     data["input_message"] = input_message

    # save_conflicting_data(finetuning_data_test_normal, output_file_test_normal)

    # # Generate ideal outputs for reversed data
    # logger.info("Generating ideal outputs for reversed training data...")
    # for data in tqdm(finetuning_data_training_reversed):
    #     ideal_output, input_message = generate_ideal_output(data, is_reversed=True)
    #     data["ideal_output"] = ideal_output
    #     data["input_message"] = input_message

    # save_conflicting_data(finetuning_data_training_reversed, output_file_training_reversed)
    
    logger.info("Generating ideal outputs for reversed test data...")
    for data in tqdm(finetuning_data_test_reversed):
        ideal_output, input_message = generate_ideal_output(data, is_reversed=True)
        data["ideal_output"] = ideal_output
        data["input_message"] = input_message

    save_conflicting_data(finetuning_data_test_reversed, output_file_test_reversed)
    
    logger.info(f"Final dataset sizes - \n"
                f"Normal Training: {len(finetuning_data_training_normal)}, \n"
                f"Normal Test: {len(finetuning_data_test_normal)}, \n"
                f"Reversed Training: {len(finetuning_data_training_reversed)}, \n"
                f"Reversed Test: {len(finetuning_data_test_reversed)}")

if __name__ == "__main__":
    main()
