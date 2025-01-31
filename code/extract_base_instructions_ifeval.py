import json
import time
import logging
from tqdm import tqdm
from pathlib import Path


root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


from llm_api import get_completion_llama3, get_completion_gpt4o



def clean_prompt(prompt, constraints):
   # load system prompt from prompt/prompt_extract_base_instruction
   system_prompt = (root_dir / 'prompt' / 'prompt_extract_base_instruction').read_text()
   return get_completion_gpt4o(system_prompt, f"Prompt: {prompt}\nConstraints: {constraints}")

def process_prompts(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    logger.info(f"Processing {len(lines)} prompts")

    output_data = []
    for line in tqdm(lines):
        data = json.loads(line)
        data['base_instruction'] = clean_prompt(data['prompt'], data['instruction_id_list'])
        output_data.append(data)
        time.sleep(1)



    with open(output_file, 'w') as f:
        for data in output_data:
            f.write(json.dumps(data) + '\n')



ifeval_input_data_path = root_dir / 'data' / 'ifeval_input_data.jsonl'
output_path = root_dir / 'data' / 'base_instructions_extracted.jsonl'
process_prompts(ifeval_input_data_path, output_path)