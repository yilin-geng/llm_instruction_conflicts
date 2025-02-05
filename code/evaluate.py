from llmclient import Next_Client
from api_keys import NEXT_BASE_URL, NEXT_API_KEY, OPENAI_API_KEY
import json
from pathlib import Path
from typing import List, Dict
import logging
from tqdm import tqdm
from datetime import datetime
from priority_control_policies import *
from llm_api import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
root_dir = Path(__file__).parent.parent

# Models to evaluate
models = [
    "qwen2.5-7b-instruct",
    # "gpt-4o-mini-2024-07-18",
    # "gpt-4o-2024-11-20",
    # "claude-3-5-sonnet-20241022",
    # "deepseek-r1"
]

# Data paths to evaluate
data_paths = [
    root_dir / 'data' / 'conflicting_instructions.jsonl',
    root_dir / 'data' / 'conflicting_instructions_reversed.jsonl',
    root_dir / 'data' / 'conflicting_instructions_rich_context.jsonl',
    root_dir / 'data' / 'conflicting_instructions_rich_context_reversed.jsonl',
]

# Initialize policies
policies = [
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

# Configuration flag
USE_NEXT_CLIENT = True  # Set to True to use Next_Client, False to use llm_api (need sperate api keys for each model)

def get_llm_call_fn(model: str):
    """Get appropriate LLM client based on configuration"""
    if USE_NEXT_CLIENT:
        api_config = {
            "NEXT_BASE_URL": NEXT_BASE_URL,
            "NEXT_API_KEY": NEXT_API_KEY,
            "OPENAI_API_KEY": OPENAI_API_KEY,
        }
        client = Next_Client(model=model, api_config=api_config)
        return client.multi_call
    else:
        # Map models to their corresponding functions
        model_map = {
            "gpt-4o-2024-11-20": lambda x: batch_llm_call(x, get_completion_gpt4o),
            "llama-3.1-70b": lambda x: batch_llm_call(x, get_completion_llama3),
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

def save_results(model: str, policy_name: str, data_path: Path, messages: List[List[Dict]], 
                responses: List[str], results: List[PolicyEvaluation], results_dir: Path, timestamp: str):
    """Save evaluation results and create experiment log."""
    experiment_dir = results_dir / timestamp
    experiment_dir.mkdir(exist_ok=True, parents=True)
    
    # Save detailed results
    dataset_name = data_path.stem
    output_file = experiment_dir / f"{dataset_name}_{model}_{policy_name}_results.jsonl"
    with open(output_file, 'w') as f:
        for message, response, result in zip(messages, responses, results):
            result_dict = {
                "model": model,
                "policy": policy_name,
                "dataset": dataset_name,
                "input_data": message,
                "response": response,
                "evaluation": {
                    "conflict_recognized": result.conflict_recognized,
                    "primary_constraint_met": result.primary_constraint_met,
                    "secondary_constraint_met": result.secondary_constraint_met,
                    "joint_satisfaction": result.joint_satisfaction,
                    "conflict_name": result.conflict_name
                }
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

    results_dir = root_dir / 'results'
    results_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_experiment_log(policies, models, data_paths, timestamp, results_dir)
    
    # Process each dataset
    for data_path in data_paths:
        logger.info(f"Processing data path: {data_path}")
        evaluation_data = load_data(data_path)
        
        # Evaluate each model
        for model in models:
            logger.info(f"Evaluating model: {model}")
            llm_call_fn = get_llm_call_fn(model)
            
            # Evaluate each policy
            for policy in tqdm(policies, desc=f"Processing policies for {model}"):
                logger.info(f"Processing policy: {policy.name}")
                messages = construct_messages(policy, evaluation_data)
                responses = llm_call_fn(messages)
                if len(responses) != len(messages):
                    logger.error(f"Mismatch between messages ({len(messages)}) and responses ({len(responses)})")
                    raise ValueError("Number of responses does not match number of messages")
                
                # Process responses
                results = policy.evaluate_responses(evaluation_data, responses, 
                                                    is_reversed='reversed' in str(data_path))
                
                # Save results
                save_results(model, policy.name, data_path, messages, responses, 
                            results, results_dir, timestamp)
            

    # # Run analysis after all evaluations are complete
    # logger.info("Starting analysis...")
    # from analyze import main as analyze_main
    # import sys
    # sys.argv = [sys.argv[0], '--timestamp', timestamp]
    # analyze_main()
    # logger.info("Analysis complete")

if __name__ == "__main__":
    main()