# Control Illusion: The Failure of Instruction Hierarchies in Large Language Models

This repository contains the code for the paper "Control Illusion: The Failure of Instruction Hierarchies in Large Language Models" (http://arxiv.org/abs/2502.15851)

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

### Processing Responses
```bash
python code/process_responses.py --target_dir <response_directory> --output_dir <processed_directory>
```

### Evaluation and Analysis
```bash
python code/analyze.py --processed_dir <response_directory> --response_type response
```

```bash
python code/analyze.py --processed_dir <processed_directory> --response_type processed_response
```