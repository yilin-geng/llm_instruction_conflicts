import json
import os
from pathlib import Path

def process_jsonl_file(file_path):
    temp_file = file_path.with_suffix('.jsonl.tmp')
    
    with open(file_path, 'r', encoding='utf-8') as f_in, \
         open(temp_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            data = json.loads(line.strip())
            # if 'evaluation' in data:
            #     del data['evaluation']
            if "training" in file_path.name and data["conflict_name"] not in ["num_sentence_conflict: 12_7", "keyword_frequency_conflict: often_6_3"]:
                f_out.write(json.dumps(data, ensure_ascii=True) + '\n')
            elif "test" in file_path.name and data["conflict_name"] in ["num_sentence_conflict: 12_7", "keyword_frequency_conflict: often_6_3"]:
                f_out.write(json.dumps(data, ensure_ascii=True) + '\n')
            else:
                print(f"Skipping {data['conflict_name']} in {file_path.name}")
    
    # Replace original file with the new one
    os.replace(temp_file, file_path)

def main():
    directory = Path('.')
    
    # Process all .jsonl files in the directory
    for file_path in directory.glob('*_normal.jsonl'):
        print(f"Processing {file_path}")
        process_jsonl_file(file_path)
        print(f"Finished processing {file_path}")

if __name__ == '__main__':
    main() 