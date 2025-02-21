# Control Illusion: The Failure of Instruction Hierarchies in Large Language Models

This repository contains the code for the paper "Control Illusion: The Failure of Instruction Hierarchies in Large Language Models" (https://arxiv.org/abs/xxxxxxx)

### Dataset Creation
python code/synthesize_conflicting_data.py
python code/synthesize_conflicting_data_rich_context.py

### Getting Responses
python code/get_responses.py
python code/process_responses.py --target_dir <response_directory> --output_dir <processed_directory>

### Evaluation and Analysis
python code/analyze.py --processed_dir <response_directory> --response_type response
python code/analyze.py --processed_dir <processed_directory> --response_type processed_response