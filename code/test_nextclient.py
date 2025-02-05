import llmclient.next_client as next_client
from api_keys import NEXT_API_KEY, NEXT_BASE_URL, OPENAI_API_KEY


api_config = {
        "NEXT_BASE_URL": NEXT_BASE_URL,
        "NEXT_API_KEY": NEXT_API_KEY,
        "OPENAI_API_KEY": OPENAI_API_KEY,
    }

models = [
    "qwen2.5-7b-instruct",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-2024-11-20",
    "claude-3-5-sonnet-20241022",
    "deepseek-r1"
]


test_data = [
    [{"role": "user", "content": "Say 1"}],
    [{"role": "user", "content": "Say 2"}],
    [{"role": "user", "content": "Say 3"}],
    [{"role": "user", "content": "Say 'Ready to go!'"}],
]

for model in models:
    print(f"Testing model: {model}")
    client = next_client.Next_Client(model=model, api_config=api_config)
    responses = client.multi_call(test_data)
    print(responses)


