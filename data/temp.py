import json
import pandas as pd
from pathlib import Path

# Set up paths
root_dir = Path(__file__).parent.parent
input_file = root_dir / 'data' / 'base_instructions.jsonl'
output_file = root_dir / 'data' / 'human_labeling.csv'

# Initialize empty list to store data
data = []

# Read the JSONL file
with open(input_file, 'r') as f:
    for line in f:
        item = json.loads(line)
        data.append({
            'base_instruction': item['base_instruction'],
            'is_valid': '',  # Empty field for human annotation
            'language_conflict': '',  # Empty field for human annotation
            'case_conflict': '',  # Empty field for human annotation
            'word_length_conflict': '',  # Empty field for human annotation
            'num_sentence_conflict': '',  # Empty field for human annotation
            'keyword_forbidden_conflict': '',  # Empty field for human annotation
            'keyword_frequency_conflict': ''  # Empty field for human annotation
        })

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv(output_file, index=False)

print(f"Created CSV file at {output_file}")
