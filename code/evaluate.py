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
    data_path = root_dir / 'data' / 'conflicting_instructions_test.jsonl' # test
    output_dir = root_dir / 'results'
    checkpoint_dir = output_dir / 'checkpoints'
    
    # Create directories
    output_dir.mkdir(exist_ok=True)
    checkpoint_dir.mkdir(exist_ok=True)

    evaluator = ConflictPolicyEvaluator(policies, llm_call_fns)

    logger.info("Starting evaluation...")
    try:
        results = evaluator.evaluate_all(data_path, checkpoint_dir)
        save_results(results, output_dir)
        logger.info(f"Results saved to {output_dir}")
    except KeyboardInterrupt:
        logger.info("Evaluation interrupted by user. Progress has been saved to checkpoint.")
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        logger.info("Partial progress has been saved to checkpoint.")

def save_results(results: Dict[str, List[PolicyEvaluation]], output_dir: Path):
    """Save evaluation results to files with timestamps."""
    output_dir.mkdir(exist_ok=True)
    
    # Add timestamp to output directory
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_dir = output_dir / timestamp
    timestamped_dir.mkdir(exist_ok=True)
    
    for llm_name, evaluations in results.items():
        output_file = timestamped_dir / f"{llm_name}_results.jsonl"
        with open(output_file, 'w') as f:
            for eval_result in evaluations:
                f.write(json.dumps(asdict(eval_result)) + '\n')

if __name__ == "__main__":
    main() 