import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from api_keys import TOGETHER_API_KEY, OPENAI_API_KEY

# Disable httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)

from together import Together
client_together = Together(api_key=TOGETHER_API_KEY)
def get_completion_llama3(system_prompt,prompt):
    response = client_together.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "system", "content": system_prompt}, 
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


import openai
client_openai = openai.OpenAI(api_key=OPENAI_API_KEY)
def get_completion_gpt4o(system_prompt,prompt):
    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}, 
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def get_completion_gpt4omini(system_prompt,prompt):
    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, 
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

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

if __name__ == "__main__":
    main()

