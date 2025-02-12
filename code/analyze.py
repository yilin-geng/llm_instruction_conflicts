from pathlib import Path
import json
import logging
import pandas as pd
from tqdm import tqdm
import argparse
from typing import Dict, List
from priority_control_policies import *
from conflicts_dict import INSTRUCTION_CONFLICTS

# Test set conflict names
# TEST_CONFLICTS = ["num_sentence_conflict: 12_7", "keyword_frequency_conflict: often_6_3"]
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


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_expected_files_mapping():
    """Generate mapping of all expected response files based on models, datasets, and policies."""
    models = [
        "qwen2.5-7b-instruct",
        "gpt-4o-mini-2024-07-18",
        "gpt-4o-2024-11-20",
        "claude-3-5-sonnet-20241022",
        "Llama-3.1-8B",
        "Llama-3.1-8B-conflict",
        "Llama-3.1-8B-conflict_0",
        "Llama-3.1-8B-conflict_1",
        "Llama-3.1-8B-conflict_2",
        "Llama-3.1-70B",
    ]
    
    datasets = [
        'conflicting_instructions',
        'conflicting_instructions_reversed',
        'conflicting_instructions_rich_context',
        'conflicting_instructions_rich_context_reversed'
    ]
    
    policies = [
        "constraint_following_baseline",
        "baseline_all_user",
        "basic_separation",
        "task_specified_separation",
        "emphasized_separation",
        "unmarked_system_basic",
        "marked_system_basic", 
        "unmarked_user_basic",
        "marked_user_basic",
        "unmarked_system_detailed",
        "marked_system_detailed",
        "unmarked_user_detailed",
        "marked_user_detailed"
    ]
    
    expected_files = {}
    for model in models:
        for dataset in datasets:
            for policy in policies:
                filename = f"{dataset}_{model}_{policy}_responses.jsonl"
                expected_files[filename] = {
                    'model': model,
                    'dataset': dataset,
                    'policy': policy
                }
    return expected_files

def load_response_files(processed_dir: Path, response_type: str = 'processed_response') -> List[Dict]:
    """Load response files from processed responses directory.
    Args:
        processed_dir: Directory containing processed response files
        response_type: Which response to analyze - 'response' or 'processed_response'
    """
    results = []
    expected_files = get_expected_files_mapping()

    existing_files = set(file.name for file in processed_dir.glob('*.jsonl'))
    # check if all expected files are present
    missing_files = set(expected_files.keys()) - existing_files
    if missing_files:
        logger.warning(f"Missing expected files: {missing_files}")
    
    for file_path in processed_dir.glob('*.jsonl'):
        filename = file_path.name
        metadata = expected_files[filename]
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    if response_type == 'processed_response':
                        try:
                            processed_response_data = json.loads(entry['processed_response'])
                            # there are multiple possible keys returned by the models
                            conflict_recognized_keys = ['conflict_recognized', 'conflict_detected']
                            for key in conflict_recognized_keys:
                                if key in processed_response_data:
                                    recognition_flag = float(processed_response_data[key])
                                    response_data = processed_response_data['processed_response']
                                    break
                        except:
                            # never happens
                            logger.warning(f"Error parsing processed response for {filename}")
                            recognition_flag = None
                            response_data = entry['response']
                    else:
                        response_data = entry['response']
                    
                    results.append({
                        'dataset': metadata['dataset'],
                        'model': metadata['model'],
                        'policy': metadata['policy'],
                        'response': response_data,
                        'conflict_recognized': recognition_flag if response_type == 'processed_response' else None
                    })
    
    return results

def evaluate_responses(df: pd.DataFrame, test_set_only: bool = False, output_index: int = 4) -> pd.DataFrame:
    """Evaluate responses using the appropriate policies and conflict definitions.
    
    Args:
        df: DataFrame containing responses to evaluate
        test_set_only: If True, only evaluate responses for test set conflicts
    """
    # Initialize policies
    policies = {
        "constraint_following_baseline": ConstraintFollowingBaseline("constraint_following_baseline"),
        "baseline_all_user": BaselineAllUserPolicy("baseline_all_user"),
        "basic_separation": BasicSeparationPolicy("basic_separation"),
        "task_specified_separation": TaskSpecifiedSeparationPolicy("task_specified_separation"),
        "emphasized_separation": EmphasizedSeparationPolicy("emphasized_separation"),
        "unmarked_system_basic": UnmarkedSystemPolicyBasic("unmarked_system_basic"),
        "marked_system_basic": MarkedSystemPolicyBasic("marked_system_basic"),
        "unmarked_user_basic": UnmarkedUserPolicyBasic("unmarked_user_basic"),
        "marked_user_basic": MarkedUserPolicyBasic("marked_user_basic"),
        "unmarked_system_detailed": UnmarkedSystemPolicyDetailed("unmarked_system_detailed"),
        "marked_system_detailed": MarkedSystemPolicyDetailed("marked_system_detailed"),
        "unmarked_user_detailed": UnmarkedUserPolicyDetailed("unmarked_user_detailed"),
        "marked_user_detailed": MarkedUserPolicyDetailed("marked_user_detailed")
    }
    
    evaluated_results = []

    data_dir = Path(__file__).parent.parent / 'data'
    
    # Group by dataset, policy, and model to evaluate each combination
    for (dataset, policy_name, model), group in df.groupby(['dataset', 'policy', 'model']):
        # Load original conflict data
        data_path = data_dir / f"{dataset}.jsonl"
        with open(data_path, 'r') as f:
            conflict_data = [json.loads(line) for line in f]
            
        # Filter conflict data and responses if test_set_only is True
        if test_set_only:
            print([data['conflict_name'] for data in conflict_data])
            test_indices = [i for i, data in enumerate(conflict_data) if data['conflict_name'] in test_conflict_names[output_index]]
            if not test_indices:  # Skip if no test conflicts found
                raise ValueError(f"No test conflicts found for model {model}, dataset {dataset}, policy {policy_name}")
            conflict_data = [conflict_data[i] for i in test_indices]
            group = group.iloc[test_indices].reset_index(drop=True)
            
        # Get policy and evaluate
        policy = policies[policy_name]
        is_reversed = 'reversed' in dataset
        evaluations = policy.evaluate_responses(conflict_data, group['response'].tolist(), is_reversed)

        # Check evaluations length matches data length
        expected_len = 200 if test_set_only else 600
        assert len(evaluations) == expected_len, f"Expected {expected_len} evaluations for model {model}, got {len(evaluations)}"

        # Store results
        for idx, eval_result in enumerate(evaluations):
            evaluated_results.append({
                'dataset': dataset,
                'policy': policy_name,
                'model': model,
                'primary_constraint_met': eval_result.primary_constraint_met,
                'secondary_constraint_met': eval_result.secondary_constraint_met,
                'both_constraint_met': eval_result.primary_constraint_met and eval_result.secondary_constraint_met,
                'none_constraint_met': not eval_result.primary_constraint_met and not eval_result.secondary_constraint_met,
                'conflict_name': eval_result.conflict_name,
                'conflict_recognized': group['conflict_recognized'].iloc[idx]  # Match recognition with corresponding response TODO: double check
            })
            
    return pd.DataFrame(evaluated_results)


def generate_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate summary statistics for the evaluated responses."""
    dataset_level_summary = df.groupby(['model', 'policy', 'dataset']).agg({
        'primary_constraint_met': 'mean',
        'secondary_constraint_met': 'mean',
        'none_constraint_met': 'mean',
        'conflict_recognized': 'mean',
    }).round(3)

    conflict_level_summary = df.groupby(['model', 'policy', 'dataset', 'conflict_name']).agg({
        'primary_constraint_met': 'mean',
        'secondary_constraint_met': 'mean',
        'none_constraint_met': 'mean',
        'conflict_recognized': 'mean',
    }).round(3)

    return dataset_level_summary, conflict_level_summary
    


def main():
    parser = argparse.ArgumentParser(description='Analyze model responses')
    parser.add_argument('--processed_dir', type=str, default='results/processed_responses',
                      help='Directory containing processed response files')
    parser.add_argument('--response_type', type=str, choices=['response', 'processed_response'],
                      default='processed_response', help='Which response to analyze')
    parser.add_argument('--test_set_only', action='store_true',
                      help='Only evaluate responses for test set conflicts')
    parser.add_argument('--output_index', type=int, default=4,
                      help='Index of the output to analyze')
    args = parser.parse_args()
    
    root_dir = Path(__file__).parent.parent
    processed_dir = root_dir / args.processed_dir
    # Create analysis directory
    analysis_dir = root_dir / 'analysis'
    analysis_dir.mkdir(exist_ok=True)
    
    # Load responses
    results_df = pd.DataFrame(load_response_files(processed_dir, args.response_type))
    logger.info(f"Loaded {len(results_df)} responses")
    
    # Evaluate responses
    evaluated_df = evaluate_responses(results_df, test_set_only=args.test_set_only, output_index=args.output_index)
    logger.info(f"Evaluated {len(evaluated_df)} responses")
    
    # Add suffix to output files if test_set_only is True
    suffix = f'_test_only_{args.output_index}' if args.test_set_only else ''
    evaluated_df.to_csv(analysis_dir / f'evaluated_{args.response_type}{suffix}.csv', index=False)

    # Generate summary
    dataset_summary, conflict_summary = generate_summary(evaluated_df)
    dataset_summary.to_csv(analysis_dir / f'dataset_level_summary_{args.response_type}{suffix}.csv')
    conflict_summary.to_csv(analysis_dir / f'conflict_level_summary_{args.response_type}{suffix}.csv')
    
    logger.info(f"Analysis complete. Results saved to {analysis_dir}")

if __name__ == "__main__":
    main()


