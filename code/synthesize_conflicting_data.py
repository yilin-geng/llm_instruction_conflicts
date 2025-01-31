import json
import logging
from pathlib import Path
from typing import Dict, List
import pandas as pd

root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from conflicts_dict import INSTRUCTION_CONFLICTS

def generate_conflicting_data(base_instructions_file: Path, flip_instructions: bool = False) -> List[Dict]:
    """Generate conflicting instruction pairs from base instructions.
    
    Args:
        base_instructions_file: Path to CSV file containing base instructions
        flip_instructions: If True, flip constraint1 and constraint2 in the output
    """
    conflicting_data = []
    
    # Read base instructions from CSV
    df = pd.read_csv(base_instructions_file)
    
    # For each base instruction
    for _, row in df.iterrows():
        base_instruction = row['base_instruction']
        
        # For each conflict type
        for conflict_name, conflict_data in INSTRUCTION_CONFLICTS.items():
            # Skip commented out conflicts
            if conflict_name.startswith('#'):
                continue
                
            conflict_pair = conflict_data["conflict_pair"]
            
            # Get the conflicting instructions
            constraint1, constraint2 = conflict_pair.get_constraints()
            
            # Flip instructions if requested
            if flip_instructions:
                constraint1, constraint2 = constraint2, constraint1
            
            # Create data point
            data_point = {
                'base_instruction': base_instruction,
                'constraint1': constraint1,
                'constraint2': constraint2,
                'kwargs': conflict_pair.kwargs if not flip_instructions else list(reversed(conflict_pair.kwargs)),
                'conflict_name': conflict_name
            }
            
            conflicting_data.append(data_point)
            logger.debug(f"Added conflict pair: {conflict_name} for base instruction: {base_instruction[:50]}...")
    
    return conflicting_data

def save_conflicting_data(data: List[Dict], output_file: Path):
    """Save conflicting instruction pairs to a JSONL file."""
    with open(output_file, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def main():
    base_instructions_file = root_dir / 'data' / 'base_instructions_picked.csv'
    output_file = root_dir / 'data' / 'conflicting_instructions.jsonl'
    output_file_reversed = root_dir / 'data' / 'conflicting_instructions_reversed.jsonl'
    
    logger.info("Generating conflicting instructions...")
    if not base_instructions_file.exists():
        logger.error(f"Input file not found: {base_instructions_file}")
        return
        
    # Generate normal conflicting data
    conflicting_data = generate_conflicting_data(base_instructions_file, flip_instructions=False)
    
    if not conflicting_data:
        logger.warning("No conflicting instructions were generated!")
        return
        
    logger.info(f"Generated {len(conflicting_data)} conflicting instruction pairs")
    save_conflicting_data(conflicting_data, output_file)
    logger.info(f"Saved conflicting instructions to {output_file}")
    
    # Generate reversed conflicting data
    conflicting_data_reversed = generate_conflicting_data(base_instructions_file, flip_instructions=True)
    save_conflicting_data(conflicting_data_reversed, output_file_reversed)
    logger.info(f"Saved reversed conflicting instructions to {output_file_reversed}")

if __name__ == "__main__":
    main()
