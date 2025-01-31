import json
import logging
from pathlib import Path
from typing import Dict, List
import time
import textwrap
import tqdm

root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from llm_api import get_completion_gpt4o

def enrich_instruction_with_context(instruction: str) -> str:
    """Use GPT-4 to add rich context to an instruction while preserving its core meaning."""
    system_prompt = """You are helping to enrich instructions with more context and details, while preserving their core meaning and constraints."""
    
    user_prompt = textwrap.dedent(f"""
        Enrich the following instruction with more context and details, while preserving its core meaning and constraints. 
        Make it more specific and detailed, but ensure it remains compatible with the original instruction.
        
        Original instruction: {instruction}
        
        Rules:
        1. Keep the same core task/request
        2. Add relevant context and details
        3. Make it more specific but compatible
        4. Preserve any implicit constraints
        5. Don't change the fundamental nature of the task
        
        Return only the enriched instruction, nothing else.
        """).strip()
    
    try:
        enriched = get_completion_gpt4o(system_prompt, user_prompt).strip()
        return enriched
    except Exception as e:
        logger.error(f"Error enriching instruction: {e}")
        return instruction

def enrich_data_point(data_point: Dict) -> Dict:
    """Enrich a single data point with richer context."""
    enriched = data_point.copy()
    
    # Enrich base instruction
    enriched['base_instruction'] = enrich_instruction_with_context(
        data_point['base_instruction']
    )
    
    # Enrich constraint1 and constraint2
    enriched['constraint1'] = enrich_instruction_with_context(
        data_point['constraint1']
    )
    enriched['constraint2'] = enrich_instruction_with_context(
        data_point['constraint2']
    )
    
    # Add metadata about enrichment
    enriched['enriched'] = True
    enriched['original_base_instruction'] = data_point['base_instruction']
    enriched['original_constraint1'] = data_point['constraint1']
    enriched['original_constraint2'] = data_point['constraint2']
    
    return enriched

def generate_rich_context_data(input_file: Path, output_file: Path):
    """Generate enriched version of conflicting instructions data."""
    enriched_data = []
    
    with open(input_file, 'r') as f:
        data = [json.loads(line) for line in f]
    
    total = len(data)
    logger.info(f"Enriching {total} data points...")
    
    for item in tqdm.tqdm(data, desc="Enriching instructions", total=total):
        enriched_item = enrich_data_point(item)
        enriched_data.append(enriched_item)
    
    with open(output_file, 'w') as f:
        for item in enriched_data:
            f.write(json.dumps(item) + '\n')
    
    return enriched_data

def create_reversed_data(enriched_data: List[Dict], output_file: Path):
    """Create reversed version of enriched data without additional API calls."""
    reversed_data = []
    
    for item in enriched_data:
        reversed_item = item.copy()
        
        # Swap constraints
        reversed_item['constraint1'], reversed_item['constraint2'] = (
            reversed_item['constraint2'],
            reversed_item['constraint1']
        )
        
        # Swap original constraints
        reversed_item['original_constraint1'], reversed_item['original_constraint2'] = (
            reversed_item['original_constraint2'],
            reversed_item['original_constraint1']
        )
        
        # Swap kwargs if present
        if 'kwargs' in reversed_item:
            reversed_item['kwargs'] = list(reversed(reversed_item['kwargs']))
            
        reversed_data.append(reversed_item)
    
    with open(output_file, 'w') as f:
        for item in reversed_data:
            f.write(json.dumps(item) + '\n')

def main():
    input_file = root_dir / 'data' / 'conflicting_instructions.jsonl'
    output_file = root_dir / 'data' / 'conflicting_instructions_rich_context.jsonl'
    output_file_reversed = root_dir / 'data' / 'conflicting_instructions_rich_context_reversed.jsonl'
    
    logger.info("Generating rich context conflicting instructions...")
    if not input_file.exists():
        logger.error(f"Input file not found: {input_file}")
        return
        
    # Generate enriched data with API calls
    enriched_data = generate_rich_context_data(input_file, output_file)
    logger.info(f"Saved rich context instructions to {output_file}")
    
    # Create reversed version without additional API calls
    create_reversed_data(enriched_data, output_file_reversed)
    logger.info(f"Saved reversed rich context instructions to {output_file_reversed}")

if __name__ == "__main__":
    main()
