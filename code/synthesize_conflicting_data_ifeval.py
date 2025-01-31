# with base instructions defined in base_instructions.py, we would like to synthesize a set of conflicting instructions.
# The conflict types are defined in conflicts.py. INSTRUCTION_CONFLICTS is a dictionary of ConflictingInstructionPair.
# The process is as follows:
# 1. For each data point in base_instructions.py, for each of the orginal instruction_id in "instruction_id_list", we find the corresponding ConflictingInstructionPair in INSTRUCTION_CONFLICTS.
# 2. We get the conflicting instructions from the ConflictingInstructionPair.
# 3. We get the corresponding base instruction from that data point in base_instructions.py.
# 4. We generate a set of data points with the conflicting instructions. The data points should be a list of dictionaries, each dictionary contains the base instruction and the two conflicting instructions, along with the kwargs and the ConflictingInstructionPair object.
# 5. We then save the data points to a file. And the file should be a jsonl file, each line is a json object.


import json
import logging
from pathlib import Path
import sys
from typing import Dict, List, Optional, Tuple

root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import instructions
from conflicts import ConflictingInstructionPair
from conflicts_dict import INSTRUCTION_CONFLICTS



def find_conflicts(instruction_id: str) -> List[str]:
    """Find all conflicting instruction IDs for a given instruction ID."""
    conflicts = []
    for conflict_name, conflict_data in INSTRUCTION_CONFLICTS.items():
        if instruction_id in conflict_data["related_instruction_ids"]:
            conflicts.append(conflict_name)
    return conflicts

def generate_conflicting_data(base_instruction_file: Path, flip_instructions: bool = False) -> List[Dict]:
    """Generate conflicting instruction pairs from base instructions.
    
    Args:
        base_instruction_file: Path to base instructions file
        flip_instructions: If True, flip instruction1 and instruction2 in the output
    """
    conflicting_data = []
    
    with open(base_instruction_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            base_instruction = data['base_instruction']
            instruction_ids = data['instruction_id_list']
            
            # For each instruction ID, find conflicts
            for inst_id in instruction_ids:
                conflicts = find_conflicts(inst_id)
                logger.debug(f"Found conflicts for {inst_id}: {conflicts}")
                
                # For each conflict, create a data point
                for conflict_name in conflicts:
                    conflict_data = INSTRUCTION_CONFLICTS[conflict_name]
                    conflict_pair = conflict_data["conflict_pair"]
                    
                    # Get the conflicting instructions - these are already descriptions
                    inst1, inst2 = conflict_pair.get_instructions()
                    
                    # Flip instructions if requested
                    if flip_instructions:
                        inst1, inst2 = inst2, inst1
                    
                    # Create data point
                    data_point = {
                        'base_instruction': base_instruction,
                        'instruction1': inst1,  # Already a description string
                        'instruction2': inst2,  # Already a description string
                        'kwargs': conflict_pair.kwargs if not flip_instructions else list(reversed(conflict_pair.kwargs)),
                        'conflict_name': conflict_name,
                        'original_instruction_id': inst_id
                    }
                    
                    conflicting_data.append(data_point)
                    logger.info(f"Added conflict pair: {conflict_name} for instruction {inst_id}")
    
    return conflicting_data

def save_conflicting_data(data: List[Dict], output_file: Path):
    """Save conflicting instruction pairs to a JSONL file."""
    with open(output_file, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def main():
    base_instruction_file = root_dir / 'data' / 'base_instructions_extracted.jsonl'
    output_file = root_dir / 'data' / 'conflicting_instructions.jsonl'
    output_file_reversed = root_dir / 'data' / 'conflicting_instructions_reversed.jsonl'
    
    logger.info("Generating conflicting instructions...")
    if not base_instruction_file.exists():
        logger.error(f"Input file not found: {base_instruction_file}")
        return
        
    # Generate normal conflicting data
    conflicting_data = generate_conflicting_data(base_instruction_file, flip_instructions=False)
    
    if not conflicting_data:
        logger.warning("No conflicting instructions were generated!")
        return
        
    logger.info(f"Generated {len(conflicting_data)} conflicting instruction pairs")
    save_conflicting_data(conflicting_data, output_file)
    logger.info(f"Saved conflicting instructions to {output_file}")
    
    # Generate reversed conflicting data
    conflicting_data_reversed = generate_conflicting_data(base_instruction_file, flip_instructions=True)
    save_conflicting_data(conflicting_data_reversed, output_file_reversed)
    logger.info(f"Saved reversed conflicting instructions to {output_file_reversed}")

if __name__ == "__main__":
    main()
