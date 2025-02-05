import logging
from typing import List, Dict
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from api_keys import TOGETHER_API_KEY, OPENAI_API_KEY

# Disable httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)

from together import Together
client_together = Together(api_key=TOGETHER_API_KEY)
def get_completion_llama3(system_prompt, messages):
    """
    Get completion from Llama 3 model
    Args:
        system_prompt: System prompt to set context
        messages: List of message dictionaries or single prompt string
    """
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    
    formatted_messages = [{"role": "system", "content": system_prompt}]
    formatted_messages.extend(messages)
    
    response = client_together.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=formatted_messages
    )
    return response.choices[0].message.content


import openai
client_openai = openai.OpenAI(api_key=OPENAI_API_KEY)
def get_completion_gpt4o(system_prompt, messages):
    """
    Get completion from GPT-4o model
    Args:
        system_prompt: System prompt to set context
        messages: List of message dictionaries or single prompt string
    """
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    
    formatted_messages = [{"role": "system", "content": system_prompt}]
    formatted_messages.extend(messages)
    
    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=formatted_messages
    )
    return response.choices[0].message.content

def get_completion_gpt4omini(system_prompt, messages):
    """
    Get completion from GPT-4o-mini model
    Args:
        system_prompt: System prompt to set context
        messages: List of message dictionaries or single prompt string
    """
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    
    formatted_messages = [{"role": "system", "content": system_prompt}]
    formatted_messages.extend(messages)
    
    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=formatted_messages
    )
    return response.choices[0].message.content

def batch_llm_call(messages_list: List[List[Dict]], llm_call_fn=get_completion_gpt4omini) -> List[str]:
    """
    Batch process messages using any LLM function
    Args:
        llm_call_fn: Function that takes (system_prompt, messages) and returns response
        messages_list: List of message lists, each containing dicts with role and content
    Returns:
        List of response strings
    """
    responses = []
    for messages in messages_list:
        system_content = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_content = next(m["content"] for m in messages if m["role"] == "user")
        response = llm_call_fn(system_content, user_content)
        responses.append(response)
    return responses

def main():
    system_prompt = "You are a helpful assistant."
    
    # Test models
    models = {
        "GPT-4o": get_completion_gpt4o,
        "GPT-4o-mini": get_completion_gpt4omini,
        "Llama-3": get_completion_llama3,
    }
    
    logger.info("Testing LLM APIs...")
    for model_name, model_func in models.items():
        try:
            prompt = f"Say 'Hello World from (whatever model you are).'"
            response = model_func(system_prompt, prompt)
            logger.info(f"{model_name} response: {response}")
        except Exception as e:
            logger.error(f"Error testing {model_name}: {e}")

    
    
    logger.info("Testing batch_llm_call...")
    messages_list = [
        [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the capital of France?"}],
        [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is the capital of Germany?"}],
    ]
    for model_name, model_func in models.items():
        logger.info(f"Testing {model_name}...")
        responses = batch_llm_call(messages_list, llm_call_fn=model_func)
        logger.info(f"Batch responses: {responses}")

if __name__ == "__main__":
    main()

