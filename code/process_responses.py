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
    system_prompt = textwrap.dedent("""
                                    You are a specialized language model focused on analyzing and processing responses from another language model (LLM-a) that was given conflicting instructions. Your primary function is to identify explicit acknowledgments of conflicts and cleanly separate them from the execution portion of responses.

                                    Core responsibilities:
                                    - Analyze responses for explicit conflict recognition
                                    - Extract clean execution content without modifying it
                                    - Produce consistent JSON output

                                    Key behaviors:
                                    - Maintain complete objectivity in processing
                                    - Never modify the execution content
                                    - Be precise in identifying explicit conflict recognition
                                    - Preserve all formatting, spacing, and special characters in the execution portion
                                    - Process responses systematically and consistently

                                    Constraints:
                                    - Do not interpret or evaluate the quality of LLM-a's responses
                                    - Do not add commentary or explanations to the processed output
                                    - Do not modify, improve, or correct the execution content
                                    - Do not make assumptions about implied conflict recognition - only identify explicit acknowledgments

                                    Output format:
                                    You must always output valid JSON with exactly two fields:
                                    - "conflict_recognized": 1 for yes and 0 for no
                                    - "processed_response": a string that is the execution part of the response without any modifications

                                    Your responses should be pure JSON without any additional text, commentary, or markdown formatting.

                                    """)
    
    messages = []
    for response in responses:
        user_prompt_requirement = textwrap.dedent("""
                                      You are tasked with analyzing responses from LLM-a that were generated from conflicting instructions. Your role is to:
                                        1. Identify if there is any explicit recognition of instruction conflicts in the response
                                        2. Extract the execution part of the response while preserving it exactly as is
                                        3. Format the output as JSON with two fields:
                                        - "conflict_recognized": boolean indicating if LLM-a explicitly acknowledged the conflict
                                        - "processed_response": string containing only the execution part, with no modifications

                                        Rules for processing:
                                        - Look for phrases that explicitly acknowledge conflicts like "I notice there are conflicting instructions", "These instructions seem to contradict", etc.
                                        - Remove only the parts that recognize/discuss the conflict
                                        - Preserve the entire execution portion exactly as written, including any formatting, code, or special characters
                                        - If there is no explicit recognition of conflicts, keep the entire response as is

                                        Output requirements:
                                        - Use valid JSON format
                                        - Always include both fields even if no conflict was recognized
                                        - Preserve all whitespace, newlines, and formatting in the processed_response

                                        Example input:
                                        "I notice these instructions conflict since you've asked for both X and Y. Here's how I'll proceed: [execution content]"

                                        Example output:
                                        {"conflict_recognized": 1, "processed_response": "[execution content]"}

                                        Example input:
                                        "Sorry, I can't do that. But here's how I'll proceed: [execution content]"

                                        Example output:
                                        {"conflict_recognized": 1, "processed_response": "[execution content]"}
                                               
                                        Example input:
                                        "Sorry, I can't do that based on your constraints."

                                        Example output:
                                        {"conflict_recognized": 1, "processed_response": ""}

                                        Example input:
                                        "[execution content]"

                                        Example output:
                                        {"conflict_recognized": 0, "processed_response": "[execution content]"}

                                        Example input:
                                        "I notice these instructions conflict since you've asked for both X and Y. How can I help you with your request?"

                                        Example output:
                                        {"conflict_recognized": 1, "processed_response": ""}
                                               
                                        Example input:
                                        ""

                                        Example output:
                                        {"conflict_recognized": 0, "processed_response": ""}

                                        """)
        
        user_prompt_task = textwrap.dedent(f"""
                                        Original response to process:
                                        {response}

                                        Output only the JSON, nothing else.
                                        """)
        
        user_prompt = user_prompt_requirement + user_prompt_task


        messages.append([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
    
    return llm_call_fn(messages, response_format={"type": "json_object"})


def get_entries_to_reprocess(file_path: Path) -> tuple[list[dict], list[int]]:
    """
    Read existing file and identify entries that need reprocessing.
    Returns tuple of (all_entries, indices_to_reprocess)
    """
    entries = []
    indices_to_reprocess = []
    
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            if line.strip():
                entry = json.loads(line)
                entries.append(entry)
                if entry.get('processed_response', {}).get('processed_response', '') == '':
                    indices_to_reprocess.append(i)
                    
    return entries, indices_to_reprocess


def main():
    results_dir = Path(__file__).parent.parent / 'results'
    output_dir = results_dir / f'processed_responses'
    output_dir.mkdir(exist_ok=True, parents=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()
    target_dir = Path(args.target_dir)
    if not target_dir.exists():
        raise ValueError(f"Target directory does not exist: {target_dir}")
    
    llm_call_fn = get_llm_call_fn(model="gpt-4o-mini-2024-07-18")
    
    logger.info(f"Processing directory: {target_dir}")
    
    for file_path in tqdm(list(target_dir.glob('*.jsonl'))):
        output_file = output_dir / file_path.name
        
        if output_file.exists():
            # Handle existing file
            entries, indices_to_reprocess = get_entries_to_reprocess(output_file)
            if not indices_to_reprocess:
                continue
                
            logger.info(f"Found {len(indices_to_reprocess)} entries to reprocess in {output_file}")
            responses_to_process = [entries[i]['response'] for i in indices_to_reprocess]
            
            # Process only the empty responses
            processed_responses = process_responses(responses_to_process, llm_call_fn)
            
            # Update the entries with new processed responses
            for idx, processed_response in zip(indices_to_reprocess, processed_responses):
                entries[idx]['processed_response'] = processed_response
                
            # Save updated entries
            with open(output_file, 'w') as f:
                for entry in entries:
                    f.write(json.dumps(entry) + '\n')
                    
        else:
            # Handle new file
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
            with open(output_file, 'w') as f:
                for entry, processed_response in zip(data, processed_responses):
                    entry['processed_response'] = processed_response
                    f.write(json.dumps(entry) + '\n')

if __name__ == "__main__":
    main()