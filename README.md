# Control Illusion: The Failure of Instruction Hierarchies in Large Language Models

This repository contains the data and the code for the paper "Control Illusion: The Failure of Instruction Hierarchies in Large Language Models" (http://arxiv.org/abs/2502.15851)

### Dataset Creation
```bash
python code/synthesize_conflicting_data.py
```

```bash
python code/synthesize_conflicting_data_rich_context.py
```

### Getting Responses
```bash
python code/get_responses.py
```
You will need to set up your favorite LLM clients in llm_api.py.

### Processing Responses
```bash
python code/process_responses.py --target_dir {response_directory} --output_dir {processed_directory}
```

### Evaluation and Analysis

On raw LLM responses:
```bash
python code/analyze.py --target_dir {response_directory} --response_type response
```
On processed LLM responses
```bash
python code/analyze.py --target_dir {processed_directory} --response_type processed_response
```

```bash
python code/make_tables.py
