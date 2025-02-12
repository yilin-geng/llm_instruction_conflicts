import json
import random
alpaca_path = "data/finetuning_data/alpaca_small.json"
output_index = 2
conflict_paths = [f"data/finetuning_data/finetuning_data_training_normal_with_policies_{output_index}.jsonl", f"data/finetuning_data/finetuning_data_training_reversed_with_policies_{output_index}.jsonl"]
def get_alpaca_data(file_path):
    results = []
    with open(file_path, 'r') as f:
        data = json.load(f)
    for item in data:
        result = {}
        result["messages"] = [{"role": "user", "content": item["instruction"] + "\n" + item["input"]}, {"role": "assistant", "content": item["output"]}]
        result["system"] = "You are a helpful assistant."
        results.append(result)
    return results

def get_conflict_data(file_paths):
    results = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            for line in f:
                item = json.loads(line)
                result = {}
                if item["ideal_output"].strip() == "":
                    continue
                item["input_message"].append({"role": "assistant", "content": item["ideal_output"]})
                if item["input_message"][0]["role"] == "system":
                    result["system"] = item["input_message"][0]["content"]
                    item["input_message"].pop(0)
                else:
                    result["system"] = "You are a helpful assistant."
                result["messages"] = item["input_message"]
                results.append(result)
    return results

alpaca_data = get_alpaca_data(alpaca_path)
conflict_data = get_conflict_data(conflict_paths)
print(conflict_data[0])

all_data = alpaca_data + conflict_data

random.seed(42)
random.shuffle(all_data)

with open(f"LLaMA-Factory/data/alpaca_conflict_instructions_{output_index}.json", 'w') as f:
    json.dump(all_data, f, indent=4)
    # for item in all_data:
    #     f.write(json.dumps(item) + "\n")
