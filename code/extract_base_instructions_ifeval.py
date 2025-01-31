import json
import time
import logging
from tqdm import tqdm
from pathlib import Path
import textwrap


root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


from llm_api import get_completion_llama3, get_completion_gpt4o



def clean_prompt(prompt, constraints):
   # load system prompt from prompt/prompt_extract_base_instruction
   system_prompt = textwrap.dedent("""
    Extract only the base instruction from this prompt by removing format/style constraints.
    Return only the cleaned base instruction with no additional text or explanation. 

    Example 1: 

    From the prompt "Write a riddle that describes the word \"key\" but doesn't use the word \"key\". Wrap all words into one JSON block. The word \"key\" should not appear in your entire reply.", 
    Knowing that the constraints are about ["detectable_format:json_format", "keywords:forbidden_words"]
    Output "Write a riddle that describes the word \"key\""

    Example 2: 

    From the prompt "make a tweet for playboy's twitter account without using capital letters. Include at least 4 hashtags, starting with '#'", 
    Knowing that the constraints are about ["change_case:english_lowercase", "keywords:letter_frequency"], 
    Output "make a tweet for playboy's twitter account"

    Example 3: 

    From the prompt "Write a resume for a fresh high school graduate who is seeking their first job. Make sure to include at least 12 placeholder represented by square brackets, such as [address], [name]." 
    Knowing that the constraints is about ["detectable_content:number_placeholders"]
    Return "Write a resume for a fresh high school graduate who is seeking their first job."

    Example 4:

    From the prompt "Write a 300+ word summary of the wikipedia page \"https://en.wikipedia.org/wiki/Raymond_III,_Count_of_Tripoli\". Do not use any commas and highlight at least 3 sections that has titles in markdown format, for example *highlighted section part 1*, *highlighted section part 2*, *highlighted section part 3*.",
    Knowing that the constraints are about ["punctuation:no_comma", "detectable_format:number_highlighted_sections", "length_constraints:number_words"]
    Return "Write a summary of the wikipedia page \"https://en.wikipedia.org/wiki/Raymond_III,_Count_of_Tripoli\.""
   """).strip()
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