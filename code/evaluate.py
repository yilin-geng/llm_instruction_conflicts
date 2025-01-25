import json
import logging
from pathlib import Path
from typing import Dict, List
from priority_control_policies import (
    DefaultRolePolicy,
    SpecifiedRolePolicy,
    DefaultNoPolicy,
    CommonSensePolicy,
    ExplicitPriorityPolicy,
    SpecialMarkerPolicy,
    ConflictPolicyEvaluator,
    save_results
)
from llm_api import get_completion_gpt4o, get_completion_llama3
from conflicts_dict import INSTRUCTION_CONFLICTS


root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    # Initialize policies
    policies = [
        DefaultRolePolicy("Default Role Policy"),
        SpecifiedRolePolicy("Specified Role Policy"),
        DefaultNoPolicy("Default No Policy"),
        CommonSensePolicy("Common Sence Policy"),
        ExplicitPriorityPolicy("Explicit Priorit Policy"),
        SpecialMarkerPolicy("Special Marker Policy")
    ]
    
    # Initialize LLM functions
    llm_call_fns = {
        "gpt4": get_completion_gpt4o,
        "llama3": get_completion_llama3
    }
    
    # paths
    data_path = root_dir / 'data' / 'conflicting_instructions.jsonl'
    # data_path = root_dir / 'data' / 'conflicting_instructions_test.jsonl'
    output_dir = root_dir / 'results'
    # output_dir.mkdir(exist_ok=True)
    

    evaluator = ConflictPolicyEvaluator(policies, llm_call_fns)

    logger.info("Starting evaluation...")
    results = evaluator.evaluate_all(data_path)
    
    save_results(results, output_dir)
    logger.info(f"Results saved to {output_dir}")
    
    print_summary(results)

def print_summary(results: Dict[str, List]):
    """Print summary statistics for each LLM and policy combination."""
    summary_path = root_dir / 'results' / 'result_summary.log'
    
    # file handler for the result summary
    file_handler = logging.FileHandler(summary_path)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    for llm_name, evaluations in results.items():
        logger.info(f"\nResults for {llm_name}:")
        
        policy_results = {}
        for eval_result in evaluations:
            if eval_result.policy_name not in policy_results:
                policy_results[eval_result.policy_name] = []
            policy_results[eval_result.policy_name].append(eval_result)
        
        for policy_name, policy_evals in policy_results.items():
            avg_primary = sum(e.primary_constraint_met for e in policy_evals) / len(policy_evals)
            avg_secondary = sum(e.secondary_constraint_met for e in policy_evals) / len(policy_evals)
            avg_recognized = sum(e.conflict_recognized for e in policy_evals) / len(policy_evals)
            avg_joint = sum(e.joint_satisfaction for e in policy_evals) / len(policy_evals)
            
            logger.info(f"\n{policy_name}:")
            logger.info(f"  Primary constraint satisfaction: {avg_primary:.2%}")
            logger.info(f"  Secondary constraint satisfaction: {avg_secondary:.2%}")
            logger.info(f"  Conflict recognition rate: {avg_recognized:.2%}")
            logger.info(f"  Joint satisfaction rate: {avg_joint:.2%}")
    
    logger.removeHandler(file_handler)

if __name__ == "__main__":
    main() 