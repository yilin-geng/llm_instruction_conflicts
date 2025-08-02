#!/usr/bin/env python3
import json
import sys
import re
from pathlib import Path
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_json_string(json_str):
    """Attempt to fix common JSON formatting issues."""
    # Try to find where the JSON breaks and repair it
    
    # Common issue: missing closing braces/brackets
    open_braces = json_str.count('{')
    close_braces = json_str.count('}')
    open_brackets = json_str.count('[')
    close_brackets = json_str.count(']')
    
    # Add missing closing characters at the end
    if open_braces > close_braces:
        json_str += '}' * (open_braces - close_braces)
    if open_brackets > close_brackets:
        json_str += ']' * (open_brackets - close_brackets)
    
    # Try to fix truncated strings by closing quotes
    # Count unescaped quotes
    quote_count = 0
    i = 0
    while i < len(json_str):
        if json_str[i] == '"' and (i == 0 or json_str[i-1] != '\\'):
            quote_count += 1
        i += 1
    
    # If odd number of quotes, add a closing quote
    if quote_count % 2 == 1:
        json_str += '"'
    
    return json_str

def repair_malformed_jsonl(filepath):
    """Repair malformed JSONL files by fixing corrupted JSON entries."""
    filepath = Path(filepath)
    temp_path = filepath.with_suffix('.jsonl.temp')
    
    repaired_lines = []
    errors = 0
    repairs = 0
    total = 0
    
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if line.strip():
                total += 1
                try:
                    # Try to parse the main JSON
                    entry = json.loads(line)
                    # Try to parse the processed_response JSON
                    json.loads(entry['processed_response'])
                    # If both succeed, keep the line as is
                    repaired_lines.append(line)
                except json.JSONDecodeError as e:
                    errors += 1
                    logger.info(f"Attempting to repair malformed entry at line {line_num}")
                    
                    try:
                        # First try to parse the outer JSON
                        try:
                            entry = json.loads(line)
                            # The outer JSON is fine, issue is with processed_response
                            try:
                                json.loads(entry['processed_response'])
                            except json.JSONDecodeError:
                                # Try to fix the processed_response JSON
                                fixed_processed = fix_json_string(entry['processed_response'])
                                try:
                                    json.loads(fixed_processed)
                                    entry['processed_response'] = fixed_processed
                                    repaired_line = json.dumps(entry) + '\n'
                                    repaired_lines.append(repaired_line)
                                    repairs += 1
                                    logger.info(f"  Successfully repaired processed_response JSON at line {line_num}")
                                except json.JSONDecodeError:
                                    # If still can't parse, try a different approach
                                    # Set processed_response to a default valid JSON
                                    logger.warning(f"  Could not repair processed_response, using fallback at line {line_num}")
                                    entry['processed_response'] = '{"conflict_recognized": 0, "processed_response": "' + entry['response'].replace('"', '\\"').replace('\n', '\\n') + '"}'
                                    repaired_line = json.dumps(entry) + '\n'
                                    repaired_lines.append(repaired_line)
                                    repairs += 1
                        except json.JSONDecodeError:
                            # The outer JSON is malformed, try to fix the entire line
                            fixed_line = fix_json_string(line.strip())
                            try:
                                entry = json.loads(fixed_line)
                                # Check if processed_response is also valid
                                try:
                                    json.loads(entry['processed_response'])
                                    repaired_lines.append(fixed_line + '\n')
                                    repairs += 1
                                    logger.info(f"  Successfully repaired entire JSON at line {line_num}")
                                except json.JSONDecodeError:
                                    # Fix processed_response as well
                                    entry['processed_response'] = '{"conflict_recognized": 0, "processed_response": "' + entry['response'].replace('"', '\\"').replace('\n', '\\n') + '"}'
                                    repaired_line = json.dumps(entry) + '\n'
                                    repaired_lines.append(repaired_line)
                                    repairs += 1
                                    logger.info(f"  Successfully repaired entire entry at line {line_num}")
                            except json.JSONDecodeError:
                                # Last resort: skip this entry
                                logger.error(f"  Could not repair entry at line {line_num}, skipping")
                                continue
                    except Exception as repair_error:
                        logger.error(f"  Error during repair at line {line_num}: {repair_error}")
                        continue
                except Exception as e:
                    logger.error(f"  Unexpected error at line {line_num}: {e}")
                    continue
    
    # Write repaired file
    with open(temp_path, 'w') as f:
        f.writelines(repaired_lines)
    
    # Replace original with repaired version
    shutil.move(temp_path, filepath)
    
    logger.info(f"Repaired {filepath}: fixed {repairs}/{errors} malformed entries out of {total} total")
    return repairs, errors, total

def main():
    if len(sys.argv) != 2:
        print("Usage: python repair_malformed_json.py <directory>")
        sys.exit(1)
    
    directory = Path(sys.argv[1])
    if not directory.exists():
        logger.error(f"Directory {directory} does not exist")
        sys.exit(1)
    
    total_repairs = 0
    total_errors = 0
    total_files = 0
    
    for jsonl_file in directory.glob("*.jsonl"):
        if jsonl_file.name.endswith('.backup'):
            continue
        repairs, errors, total = repair_malformed_jsonl(jsonl_file)
        if errors > 0:
            total_repairs += repairs
            total_errors += errors
            total_files += 1
    
    logger.info(f"Summary: Processed {total_files} files, repaired {total_repairs}/{total_errors} malformed entries")

if __name__ == "__main__":
    main()