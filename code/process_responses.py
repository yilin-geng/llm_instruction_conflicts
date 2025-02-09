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


def process_responses(responses: list[str], llm_call_fn) -> list[str]:
    system_prompt = """You are processing LLM responses to remove parts that explicitly recognize conflicts between instructions, keeping only the actual response to the task unmodified. Return only the processed response, nothing else."""
    
    messages = []
    for response in responses:
        user_prompt = f"""
        Original response:
        {response}
        
        Remove any parts that explicitly mention or discuss conflicts between instructions. Keep only the actual response to the task and keep it unmodified.
        """
        messages.append([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
    
    return llm_call_fn(messages)

def main():
    results_dir = Path(__file__).parent.parent / 'results'
    output_dir = results_dir / f'processed_responses'
    output_dir.mkdir(exist_ok=True, parents=True)


    # take target_dir as argument when calling the script with --target_dir
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()
    target_dir = Path(args.target_dir)
    if not target_dir.exists():
        raise ValueError(f"Target directory does not exist: {target_dir}")
    
    llm_call_fn = get_llm_call_fn(model="gpt-4o-mini-2024-07-18")
    

    logger.info(f"Processing directory: {target_dir}")
    
    for file_path in tqdm(list(target_dir.glob('*.jsonl'))):
        responses = []
        data = []
        
        # Read responses from file
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    responses.append(entry['response'])
                    data.append(entry)
        
        if not responses:
            continue
            
        # Process responses in batch
        processed_responses = process_responses(responses, llm_call_fn)
        
        # Save processed responses
        output_file = output_dir / file_path.name
        with open(output_file, 'w') as f:
            for entry, processed_response in zip(data, processed_responses):
                entry['processed_response'] = processed_response
                f.write(json.dumps(entry) + '\n')

if __name__ == "__main__":
    main()