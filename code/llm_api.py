import logging
import openai
from typing import List, Dict
import asyncio
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from api_keys import TOGETHER_API_KEY, OPENAI_API_KEY

# Disable httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)

from together import Together
client_together = Together(api_key=TOGETHER_API_KEY)

def create_retry_decorator(max_retries=8, min_wait=1, max_wait=60):
    return retry(
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=min_wait, max=max_wait),
        retry=retry_if_exception_type((
            openai.RateLimitError,  # Rate limit error
            openai.APITimeoutError,  # Timeout error
            openai.APIConnectionError,  # Connection error
            openai.APIError,  # Generic API error
            asyncio.TimeoutError,  # Async timeout
            TimeoutError,  # General timeout
            ConnectionError,  # Connection issues
        )),
        before_sleep=lambda retry_state: logger.warning(
            f"API call failed with {retry_state.outcome.exception()}, "
            f"retrying in {retry_state.next_action.sleep} seconds..."
        )
    )

@create_retry_decorator()
def get_completion_llama3(system_prompt, messages):
    """
    Get completion from Llama 3 model with automatic retries
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

def get_completion_openai_fn(model_name, url):
    client_openai = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=url)
    
    @create_retry_decorator()
    def get_completion_openai(system_prompt, messages):
        """
        Get completion from OpenAI-compatible model with automatic retries
        Args:
            system_prompt: System prompt to set context
            messages: List of message dictionaries or single prompt string
            model_name: Name of the model to use
        """
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        formatted_messages = [{"role": "system", "content": system_prompt}]
        formatted_messages.extend(messages)
        
        response = client_openai.chat.completions.create(
            model=model_name,
            messages=formatted_messages
        )
        return response.choices[0].message.content
    return get_completion_openai

def get_completion_openai_fn_async(model_name, url):
    client_openai = openai.AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=url)
    
    @create_retry_decorator()
    async def get_completion_openai_async(system_prompt, messages):
        """
        Get completion from OpenAI-compatible model asynchronously with automatic retries
        Args:
            system_prompt: System prompt to set context
            messages: List of message dictionaries or single prompt string
            model_name: Name of the model to use
        """
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        formatted_messages = [{"role": "system", "content": system_prompt}]
        formatted_messages.extend(messages)
        
        response = await client_openai.chat.completions.create(
            model=model_name,
            messages=formatted_messages
        )
        return response.choices[0].message.content
    return get_completion_openai_async

get_completion_gpt4omini = get_completion_openai_fn("gpt-4o-mini", "https://api.openai.com/v1")
get_completion_gpt4o = get_completion_openai_fn("gpt-4o", "https://api.openai.com/v1")

get_completion_gpt4omini_async = get_completion_openai_fn_async("gpt-4o-mini", "https://api.openai.com/v1")
get_completion_gpt4o_async = get_completion_openai_fn_async("gpt-4o", "https://api.openai.com/v1")

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
        "Llama-3-8B": get_completion_openai_fn("meta-llama/Meta-Llama-3-8B-Instruct", "http://localhost:8000/v1"),
        "Llama-3.1-8B": get_completion_openai_fn("meta-llama/Llama-3.1-8B-Instruct", "http://localhost:8000/v1"),
        "Llama-3.1-70B": get_completion_openai_fn("meta-llama/Llama-3.1-70B-Instruct", "http://localhost:8000/v1"),
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

