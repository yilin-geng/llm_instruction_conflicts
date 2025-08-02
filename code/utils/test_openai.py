import llmclient.openai_client as openai_client
from api_keys import OPENAI_API_KEY

api_config = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
}

test_data = [
    [{"role": "user", "content": "Say 1"}],
    [{"role": "user", "content": "Say 2"}],
    [{"role": "user", "content": "Say 3"}],
    [{"role": "user", "content": "Say 'Ready to go!'"}],
]

print("Testing OpenAI API directly...")
client = openai_client.OpenAI_Client(model="gpt-4o-mini-2024-07-18", api_config=api_config)
responses = client.multi_call(test_data)
print("Responses:", responses) 