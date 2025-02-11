import os
from llmclient import Next_Client, OpenAI_Client
from api_keys import NEXT_BASE_URL, NEXT_API_KEY, OPENAI_API_KEY
import json
from pathlib import Path
from typing import List, Dict
import logging
from tqdm import tqdm
from datetime import datetime
import argparse
from priority_control_policies import *
from llm_api import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
root_dir = Path(__file__).parent.parent



# Configuration flag
USE_NEXT_CLIENT = True  # Set to True to use Next_Client, False to use llm_api (need sperate api keys for each model)


# Models to evaluate
models = [
    "qwen2.5-7b-instruct",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-2024-11-20",
    "claude-3-5-sonnet-20241022",
    # "deepseek-r1"
    "Llama-3.1-8B",
    "Llama-3.1-70B",
]
model_name_mapping = {
    "Llama-3.1-8B": "meta-llama/Llama-3.1-8B-Instruct",
    "Llama-3.1-70B": "meta-llama/Llama-3.1-70B-Instruct",
    "Llama-3.1-8B-conflict": "Llama-3.1-8B-Instruct-conflict",
}

# Data paths to evaluate
data_paths = [
    root_dir / 'data' / 'conflicting_instructions.jsonl',
    root_dir / 'data' / 'conflicting_instructions_reversed.jsonl',
    root_dir / 'data' / 'conflicting_instructions_rich_context.jsonl',
    root_dir / 'data' / 'conflicting_instructions_rich_context_reversed.jsonl',
]

# Initialize policies
policies = [
    ConstraintFollowingBaseline("constraint_following_baseline"),
    BaselineAllUserPolicy("baseline_all_user"),
    BasicSeparationPolicy("basic_separation"),
    TaskSpecifiedSeparationPolicy("task_specified_separation"), 
    EmphasizedSeparationPolicy("emphasized_separation"),
    UnmarkedSystemPolicyBasic("unmarked_system_basic"),
    MarkedSystemPolicyBasic("marked_system_basic"),
    UnmarkedUserPolicyBasic("unmarked_user_basic"),
    MarkedUserPolicyBasic("marked_user_basic"),
    UnmarkedSystemPolicyDetailed("unmarked_system_detailed"),
    MarkedSystemPolicyDetailed("marked_system_detailed"),
    UnmarkedUserPolicyDetailed("unmarked_user_detailed"),
    MarkedUserPolicyDetailed("marked_user_detailed"),
]


def get_llm_call_fn(model: str, next_base_url: str = NEXT_BASE_URL, max_requests_per_minute: int = 20):
    """Get appropriate LLM client based on configuration"""
    if USE_NEXT_CLIENT:
        api_config = {
            "NEXT_BASE_URL": next_base_url,
            "NEXT_API_KEY": NEXT_API_KEY,
            "OPENAI_API_KEY": OPENAI_API_KEY,
        }
        if model in model_name_mapping:
            model = model_name_mapping[model]
        client = Next_Client(model=model, api_config=api_config, max_requests_per_minute=max_requests_per_minute)
        return client.multi_call
    else:
        # TODO: Map models to their corresponding functions (MUST MODIFY IF NOT USING OPENAI_NEXT CLIENT)
        model_map = {
            "gpt-4o-2024-11-20": lambda x: batch_llm_call(x, get_completion_gpt4o),
            # "llama-3.1-70b": lambda x: batch_llm_call(x, get_completion_llama3),
            # Add corresponding model mappings for models added in llm_api.py
        }
        return model_map.get(model, lambda x: batch_llm_call(x, get_completion_gpt4o))

def load_data(data_path: Path) -> List[Dict]:
    """Load evaluation data from jsonl file."""
    data = []
    with open(data_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def construct_messages(policy: PriorityControlPolicy, evaluation_data: List[Dict]) -> List[List[Dict]]:
    """Construct messages for batch processing."""
    conflict_data, prompts = policy.prepare_evaluation_batch(evaluation_data)
    
    messages = []
    for system_prompt, user_prompt in prompts:
        message = []
        if system_prompt:
            message.append({"role": "system", "content": system_prompt})
        message.append({"role": "user", "content": user_prompt})
        messages.append(message)
        
    return messages

def get_output_file(model: str, policy_name: str, data_path: Path, results_dir: Path, timestamp: str, temperature: float):
    experiment_dir = results_dir / timestamp
    experiment_dir.mkdir(exist_ok=True, parents=True)
    
    # Save detailed results
    dataset_name = data_path.stem
    output_file = experiment_dir / f"{dataset_name}_{model}_{policy_name}_{str(temperature)}_results.jsonl"
    return output_file

def save_responses(model: str, policy_name: str, data_path: Path, messages: List[List[Dict]], 
                responses: List[str], 
                # results: List[PolicyEvaluation], 
                results_dir: Path, timestamp: str, temperature: float):
    """Save evaluation results and create experiment log."""
    # Check for empty responses
    empty_responses = sum(1 for r in responses if not r or r.strip() == '')
    empty_ratio = empty_responses / len(responses) if responses else 1.0
    
    if empty_ratio > 0.5:
        logger.warning(f"Skipping saving results for {model} {policy_name} on {data_path.stem} - "
                      f"too many empty responses ({empty_ratio:.2%})")
        return
        
    output_file = get_output_file(model, policy_name, data_path, results_dir, timestamp, temperature)
    with open(output_file, 'w') as f:
        for message, response in zip(messages, responses):
            result_dict = {
                "model": model,
                "policy": policy_name,
                "dataset": data_path.stem,
                "input_data": message,
                "response": response,
            }
            f.write(json.dumps(result_dict) + '\n')

def save_experiment_log(policies: List[PriorityControlPolicy], models: List[str], 
                       data_paths: List[Path], timestamp: str, results_dir: Path):
    """Save experiment configuration to a log file."""
    experiment_dir = results_dir / timestamp
    experiment_dir.mkdir(exist_ok=True)
    log_file = experiment_dir / f'experiment_log_{timestamp}.txt'
    
    with open(log_file, 'w') as f:
        f.write("Experiment Configuration\n")
        f.write("======================\n\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        
        f.write("Policies:\n")
        for policy in policies:
            f.write(f"- {policy.name}\n")
        f.write("\n")
        
        f.write("Models:\n")
        for model in models:
            f.write(f"- {model}\n")
        f.write("\n")
        
        f.write("Input Data:\n")
        for data_path in data_paths:
            f.write(f"- {data_path}\n")
        f.write("\n")

def main():
    parser = argparse.ArgumentParser(description='Evaluate LLM models with different policies')
    parser.add_argument('--model', type=str, default="Llama-3.1-8B",
                        choices=list(model_name_mapping.keys()) + ["qwen2.5-7b-instruct", "gpt-4o-mini-2024-07-18", "gpt-4o-2024-11-20", "claude-3-5-sonnet-20241022", "deepseek-r1"],
                        help='Model to evaluate (default: Llama-3.1-8B)')
    parser.add_argument('--timestamp', type=str,
                        default=datetime.now().strftime("%Y%m%d_%H%M%S"),
                        help='Timestamp for the experiment (format: YYYYMMDD_HHMMSS)')
    parser.add_argument('--next-base-url', type=str,
                        default=NEXT_BASE_URL,
                        help='Base URL for the Next API')
    parser.add_argument('--temperature', type=float,
                        default=0.6,
                        help='Temperature for LLM sampling (default: 0.6)')
    parser.add_argument('--max-requests-per-minute', type=int,
                        default=100,
                        help='Maximum requests per minute for the Next API (default: 100)')
    args = parser.parse_args()

    results_dir = root_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    
    # Use command line arguments
    models = [args.model]
    timestamp = args.timestamp
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # timestamp = "20250205_110356" # 70B
    # timestamp = "20250205_091309" # 8B
    
    save_experiment_log(policies, models, data_paths, timestamp, results_dir)
    
    # Process each dataset
    for data_path in data_paths:
        logger.info(f"Processing data path: {data_path}")
        evaluation_data = load_data(data_path)
        
        # Evaluate each model
        for model in models:
            logger.info(f"Evaluating model: {model}")
            llm_call_fn = get_llm_call_fn(model, next_base_url=args.next_base_url, max_requests_per_minute=args.max_requests_per_minute)
            
            # Evaluate each policy
            for policy in tqdm(policies, desc=f"Processing policies for {model}"):
                output_file = get_output_file(model, policy.name, data_path, results_dir, timestamp, args.temperature)
                if os.path.exists(output_file):
                    logger.info(f"Skipping policy {output_file} as it already exists")
                    continue
                
                logger.info(f"Processing policy: {policy.name}")
                messages = construct_messages(policy, evaluation_data)
                responses = llm_call_fn(messages, temperature=args.temperature)
                if len(responses) != len(messages):
                    logger.error(f"Mismatch between messages ({len(messages)}) and responses ({len(responses)})")
                    raise ValueError("Number of responses does not match number of messages")
                
                # # Process responses
                # results = policy.evaluate_responses(evaluation_data, responses, 
                #                                     is_reversed='reversed' in str(data_path))
                
                # Save responses
                save_responses(model, policy.name, data_path, messages, responses, 
                            results_dir, timestamp, args.temperature)

            # leave the evaluation and analysis for later

if __name__ == "__main__":
    main()