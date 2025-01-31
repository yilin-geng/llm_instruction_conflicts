import json
import logging
from pathlib import Path
from typing import Dict, List
from priority_control_policies import *
from llm_api import get_completion_gpt4o, get_completion_llama3
from conflicts_dict import INSTRUCTION_CONFLICTS


root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():

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
    
    # Initialize LLM functions
    llm_call_fns = {
        # "gpt4": get_completion_gpt4o,
        "llama3": get_completion_llama3
    }
    
    # paths
    # data_path = root_dir / 'data' / 'conflicting_instructions.jsonl'
     # data_path = root_dir / 'data' / 'conflicting_instructions_reversed.jsonl'
    data_path = root_dir / 'data' / 'conflicting_instructions_test.jsonl' # test
    data_path = root_dir / 'data' / 'conflicting_instructions_reversed_test.jsonl' # reversed_test
    output_dir = root_dir / 'results'
    checkpoint_dir = output_dir / 'checkpoints'
    
    # Create directories
    output_dir.mkdir(exist_ok=True)
    checkpoint_dir.mkdir(exist_ok=True)

    evaluator = ConflictPolicyEvaluator(policies, llm_call_fns)

    logger.info("Starting evaluation...")
    try:
        results = evaluator.evaluate_all(data_path, checkpoint_dir)
        save_results(policies, llm_call_fns, data_path, results, output_dir)
        logger.info(f"Results saved to {output_dir}")
        
        # Delete checkpoint file after successful evaluation
        checkpoint_file = checkpoint_dir / 'evaluation_checkpoint.json'
        if checkpoint_file.exists():
            checkpoint_file.unlink()
            logger.info("Checkpoint file deleted after successful evaluation")
            
    except KeyboardInterrupt:
        logger.info("Evaluation interrupted by user. Progress has been saved to checkpoint.")
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        logger.info("Partial progress has been saved to checkpoint.")

def save_results(policies, llm_call_fns, data_path, results: Dict[str, List[PolicyEvaluation]], output_dir: Path):
    """Save evaluation results to files with timestamps."""
    output_dir.mkdir(exist_ok=True)
    
    # Add timestamp to output directory
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_dir = output_dir / timestamp
    timestamped_dir.mkdir(exist_ok=True)
    
    # Save experiment log
    save_experiment_log(policies, llm_call_fns, data_path, timestamp, timestamped_dir)
    
    for llm_name, evaluations in results.items():
        output_file = timestamped_dir / f"{llm_name}_results.jsonl"
        with open(output_file, 'w') as f:
            for eval_result in evaluations:
                f.write(json.dumps(asdict(eval_result)) + '\n')

def save_experiment_log(policies, llm_call_fns, data_path, timestamp, timestamped_dir: Path):
    """Save experiment configuration to a log file."""
    
    log_file = timestamped_dir/ f'experiment_log_{timestamp}.txt'
    
    with open(log_file, 'w') as f:
        f.write("Experiment Configuration\n")
        f.write("======================\n\n")
        
        # Log timestamp
        f.write(f"Timestamp: {timestamp}\n\n")
        
        # Log policies
        f.write("Policies:\n")
        for policy in policies:
            f.write(f"- {policy.name}\n")
        f.write("\n")
        
        # Log models
        f.write("Models:\n")
        for model_name in llm_call_fns.keys():
            f.write(f"- {model_name}\n")
        f.write("\n")
        
        # Log data path
        f.write(f"Input Data: {data_path}\n")

if __name__ == "__main__":
    main() 