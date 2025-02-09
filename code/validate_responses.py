from pathlib import Path
from llmclient import Next_Client
from api_keys import NEXT_BASE_URL, NEXT_API_KEY, OPENAI_API_KEY
import json
import logging
import textwrap
from tqdm import tqdm
from datetime import datetime
from evaluate import get_llm_call_fn
import argparse
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def validate_responses(responses: list[str]):
    empty_count = 0
    total_count = len(responses)
    empty_indices = []
    
    for i, response in enumerate(responses):
        if not response or response.strip() == '':
            empty_count += 1
            empty_indices.append(i)
            
    if total_count > 0:
        empty_ratio = empty_count / total_count
        if empty_ratio > 0:
            logger.warning(f"Found {empty_count}/{total_count} ({empty_ratio:.2%}) empty responses")
    
    return empty_count, total_count, empty_indices

def get_expected_files_mapping():
    """Generate mapping of all expected response files based on models, datasets, and policies."""
    # Extract from evaluate.py configurations
    models = [
        "qwen2.5-7b-instruct",
        "gpt-4o-mini-2024-07-18",
        "gpt-4o-2024-11-20",
        "claude-3-5-sonnet-20241022",
        "deepseek-r1",
        "Llama-3.1-8B",
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
                    'policy': policy,
                    'exists': False,
                    'empty_count': 0,
                    'total_count': 0,
                    'empty_ratio': 0.0
                }
    
    return expected_files

def fill_empty_responses(file_path: Path, empty_indices: list[int], data: list[dict], model: str, next_base_url: str):
    """Fill empty responses using the model."""
    if not empty_indices:
        return data
        
    logger.info(f"Filling {len(empty_indices)} empty responses in {file_path.name}")
    
    # Get model call function
    llm_call_fn = get_llm_call_fn(model, next_base_url=next_base_url)
    
    # Prepare messages for empty responses
    messages = []
    for idx in empty_indices:
        input_data = data[idx]['input_data']
        messages.append(input_data)
    
    # Get new responses
    new_responses = llm_call_fn(messages)
    
    # Fill empty responses
    for idx, new_response in zip(empty_indices, new_responses):
        data[idx]['response'] = new_response
        
    return data

def main():
    results_dir = Path(__file__).parent.parent / 'results'
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    parser.add_argument("--tofill", action="store_true", help="Fill empty responses if set")
    parser.add_argument("--next_base_url", type=str, default=NEXT_BASE_URL, help="Base URL for the Next API")
    args = parser.parse_args()
    target_dir = Path(args.target_dir)
    if not target_dir.exists():
        raise ValueError(f"Target directory does not exist: {target_dir}")

    logger.info(f"Processing directory: {target_dir}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = target_dir / f"empty_responses_summary_{timestamp}.log"
    
    # Get mapping of all expected files
    expected_files = get_expected_files_mapping()
    
    # Process existing files
    summary = []
    for file_path in tqdm(list(target_dir.glob('*.jsonl'))):
        data = []
        filename = file_path.name
        
        # Skip if file not in expected mapping
        if filename not in expected_files:
            logger.warning(f"Unexpected file found: {filename}")
            continue
        else:
            expected_files[filename]['exists'] = True   
            
        # Read responses from file
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    data.append(entry)
        
        if not data:
            continue
            
        # Extract responses
        responses = [entry['response'] for entry in data]
        
        # Count empty responses
        empty_count, total_count, empty_indices = validate_responses(responses)
        
        if empty_indices:
            summary_entry = {
                'file': filename,
                'empty_count': empty_count,
                'total_count': total_count,
                'empty_indices': empty_indices
            }
            summary.append(summary_entry)
            
            if args.tofill:
                # Get model name from filename
                model = expected_files[filename]['model']
                
                # Fill empty responses
                updated_data = fill_empty_responses(file_path, empty_indices, data, model, args.next_base_url)
                
                # Save updated file
                with open(file_path, 'w') as f:
                    for entry in updated_data:
                        f.write(json.dumps(entry) + '\n')
                
                summary_entry['filled'] = True
    
    # Write summary to log file
    with open(log_file, 'w') as f:
        f.write(f"Empty Response Summary - {timestamp}\n")
        f.write(f"Fill mode: {'enabled' if args.tofill else 'disabled'}\n")
        f.write("-" * 50 + "\n\n")
        
        # Missing files
        missing_files = [f for f, info in expected_files.items() if not info['exists']]
        f.write(f"Missing files ({len(missing_files)}/{len(expected_files)}):\n")
        for filename in missing_files:
            info = expected_files[filename]
            f.write(f"- {filename} (Model: {info['model']}, Dataset: {info['dataset']}, Policy: {info['policy']})\n")
        
        f.write("\n" + "-" * 50 + "\n\n")
        
        # Files with empty responses
        f.write(f"Files with empty responses ({len(summary)}):\n")
        for entry in sorted(summary, key=lambda x: x['empty_count'], reverse=True):
            f.write(f"\nFile: {entry['file']}\n")
            f.write(f"Empty responses: {entry['empty_count']}/{entry['total_count']} ")
            f.write(f"({entry['empty_count']/entry['total_count']:.2%})\n")
            f.write(f"Empty indices: {entry['empty_indices']}\n")
            if args.tofill:
                f.write(f"Status: {'Filled' if entry.get('filled') else 'Failed to fill'}\n")
    
    logger.info(f"Summary written to {log_file}")

if __name__ == "__main__":
    main()