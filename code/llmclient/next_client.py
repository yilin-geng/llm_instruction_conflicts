from openai import OpenAI
from .base import MODEL_LIST
from .openai_client import OpenAI_Client


name_mapping = {
    # openai: https://platform.openai.com/docs/models
    # "o1-2024-12-17": "o1-2024-12-17",
    # "o1-mini-2024-09-12": "o1-mini-2024-09-12",
    # "gpt-4o-2024-08-06": "gpt-4o-2024-08-06",
    # "gpt-4o-2024-05-13": "gpt-4o-2024-05-13",
    # "gpt-4o-mini-2024-07-18": "gpt-4o-mini-2024-07-18",
    # "o1-preview-2024-09-12": "o1-preview-2024-09-12",
    # "o1-mini-2024-09-12": "o1-mini-2024-09-12",
    # "gpt-4-turbo-2024-04-09": "gpt-4-turbo-2024-04-09",
    # "gpt-4-0125-preview": "gpt-4-0125-preview",
    # "gpt-4-1106-preview": "gpt-4-1106-preview",
    # "gpt-4-0613": "gpt-4-0613",
    # "gpt-3.5-turbo-0125": "gpt-3.5-turbo-0125",
    # "gpt-3.5-turbo-1106": "gpt-3.5-turbo-1106",
    # "gpt-3.5-turbo-0613": "gpt-3.5-turbo-0613",
    # anthropic: https://docs.anthropic.com/en/docs/about-claude/models
    # "claude-3-5-sonnet-20241022": "claude-3-5-sonnet-20241022",
    # "claude-3-5-haiku-20241022": "claude-3-5-haiku-20241022",
    # "claude-3-opus-20240229": "claude-3-opus-20240229",
    # "claude-3-sonnet-20240229": "claude-3-sonnet-20240229",
    # "claude-3-haiku-20240307": "claude-3-haiku-20240307",
    # # meta
    # "meta-llama/Llama-3.2-3B-Instruct": "llama-3.2-3b-instruct",
    # "meta-llama/Llama-3.2-1B-Instruct": "llama-3.2-1b-instruct",
    # "meta-llama/Llama-3.1-8B-Instruct": "llama-3.1-8b-instant",
    # "meta-llama/Llama-3.1-70B-Instruct",
    # "meta-llama/Meta-Llama-3-8B-Instruct",
    # "meta-llama/Meta-Llama-3-70B-Instruct",
    # "meta-llama/Llama-2-7b-chat-hf",
    # "meta-llama/Llama-2-13b-chat-hf",
    # "meta-llama/Llama-2-70b-chat-hf",
    # "meta-llama/CodeLlama-70b-Instruct-hf": "codellama-70b-instruct",
    # "meta-llama/CodeLlama-34b-Instruct-hf",
    # "meta-llama/CodeLlama-13b-Instruct-hf",
    # "meta-llama/CodeLlama-7b-Instruct-hf",
    # moonshot: https://platform.moonshot.cn/docs/pricing/chat#%E4%BA%A7%E5%93%81%E5%AE%9A%E4%BB%B7
    # "moonshot-v1-8k": "moonshot-v1-8k",
    # "moonshot-v1-32k": "moonshot-v1-32k",
    # "moonshot-v1-128k": "moonshot-v1-128k",
    # mistral: https://docs.mistral.ai/getting-started/models/models_overview/#tag/batch/operation/jobs_api_routes_batch_cancel_batch_job
    # "mistralai/Mixtral-8x7B-Instruct-v0.1": "mixtral-8x7b-instruct",
    # "mistralai/Mixtral-8x22B-Instruct-v0.1",
    # "mistralai/Mistral-7B-Instruct-v0.1",
    # "mistralai/Mistral-7B-Instruct-v0.2",
    # "mistralai/Mistral-7B-Instruct-v0.3",
    # "mistralai/Mistral-Nemo-Instruct-2407",
    # alibaba: https://huggingface.co/Qwen
    # "Qwen/Qwen2.5-72B-Instruct",
    # "Qwen/Qwen2.5-32B-Instruct",
    # "Qwen/Qwen2.5-14B-Instruct",
    # "Qwen/Qwen2.5-7B-Instruct",
    # "Qwen/Qwen2.5-3B-Instruct",
    # "Qwen/Qwen2.5-1.5B-Instruct",
    # "Qwen/Qwen2.5-0.5B-Instruct",
    # "Qwen/Qwen2.5-Coder-32B-Instruct",
    # "Qwen/Qwen2.5-Coder-14B-Instruct",
    # "Qwen/Qwen2.5-Coder-7B-Instruct",
    # "Qwen/Qwen2.5-Coder-3B-Instruct",
    # "Qwen/Qwen2.5-Coder-1.5B-Instruct",
    # "Qwen/Qwen2.5-Coder-0.5B-Instruct",
    # "Qwen/Qwen2.5-Coder-3B-Instruct",
    # "Qwen/Qwen2.5-Math-72B-Instruct",
    # "Qwen/Qwen2.5-Math-7B-Instruct",
    # "Qwen/Qwen2.5-Math-1.5B-Instruct",
    # "Qwen/Qwen2-72B-Instruct",
    # "Qwen/Qwen2-7B-Instruct",
    # "Qwen/Qwen2-1.5B-Instruct",
    # "Qwen/Qwen2-0.5B-Instruct",
    # "Qwen/Qwen2-Math-72B-Instruct",
    # "Qwen/Qwen2-Math-7B-Instruct",
    # "Qwen/Qwen2-Math-1.5B-Instruct",
    # "Qwen/Qwen1.5-72B-Chat",
    # "Qwen/Qwen1.5-32B-Chat",
    # "Qwen/Qwen1.5-14B-Chat",
    # "Qwen/Qwen1.5-7B-Chat",
    # "Qwen/Qwen1.5-4B-Chat",
    # "Qwen/Qwen1.5-1.8B-Chat",
    # "Qwen/Qwen1.5-0.5B-Chat",
    # "Qwen/Qwen-72B-Chat",
    # "Qwen/Qwen-14B-Chat",
    # "Qwen/Qwen-7B-Chat",
    # Qwen Commercial: https://www.alibabacloud.com/help/en/model-studio/developer-reference/use-qwen-by-calling-api?spm=a2c63.p38356.0.0.c03973b5ufdoJe
    # "qwen-max": "qwen-max",
    # "qwen-plus": "qwen-plus",
    # "qwen-turbo": "qwen-turbo",
    # google: https://ai.google.dev/gemini-api/docs/models/gemini#gemini-1.5-pro
    # "gemini-1.5-pro": "gemini-1.5-pro",
    # "gemini-1.5-flash": "gemini-1.5-flash",
    # "gemini-1.5-flash-8b",
    # "gemini-1.0-pro",
    # "google/gemma-2-27b-it",
    # "google/gemma-2-9b-it": "gemma2-9b-it",
    # "google/gemma-2-2b-it",
    # deepseek
    # "deepseek-chat": "deepseek-chat",
    # "deepseek-ai/DeepSeek-R1": "deepSeek-r1",
    # "deepseek-reasoner": "deepseek-reasoner",
    # "deepseek-ai/DeepSeek-V2-Chat",
    # "deepseek-ai/DeepSeek-V2-Lite-Chat",
    # "deepseek-ai/DeepSeek-Coder-V2-Instruct",
    # "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
    # "deepseek-ai/deepseek-llm-67b-chat",
    # "deepseek-ai/deepseek-llm-7b-chat",
    # "deepseek-ai/deepseek-coder-33b-instruct",
    # "deepseek-ai/deepseek-coder-6.7b-instruct",
    # "deepseek-ai/deepseek-coder-1.3b-instruct",
    # "deepseek-ai/deepseek-math-7b-instruct"
    # zhipu: https://bigmodel.cn/pricing
    # "GLM-4-Plus",
    # "GLM-4-0520": "glm-4-0520",
    # "GLM-4-Air": "glm-4-air",
    # "GLM-4-Flash": "glm-4-flash",
    # 01: https://platform.lingyiwanwu.com/docs#%E6%A8%A1%E5%9E%8B%E4%B8%8E%E8%AE%A1%E8%B4%B9
    #"yi-lightning",
    # "yi-large": "yi-large",
    # "yi-medium": "yi-medium",
    # "yi-spark": "yi-spark",

    # for this project
    "qwen2.5-7b-instruct": "qwen2.5-7b-instruct",
    "gpt-4o-mini-2024-07-18": "gpt-4o-mini-2024-07-18",
    "gpt-4o-2024-11-20": "gpt-4o-2024-11-20",
    "claude-3-5-sonnet-20241022": "claude-3-5-sonnet-20241022",
    "deepseek-r1": "deepseek-r1",
    "meta-llama/Llama-3.1-8B-Instruct": "meta-llama/Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.1-70B-Instruct": "meta-llama/Llama-3.1-70B-Instruct",
}



class Next_Client(OpenAI_Client):
    def __init__(
        self,
        model: str = "gpt-4-turbo",
        api_config: dict = None,
        max_requests_per_minute=20,
        request_window=20,
    ):
        super().__init__(model, api_config, max_requests_per_minute, request_window)
        self.client_name = "Next"
        self.client = OpenAI(
            base_url=self.api_config["NEXT_BASE_URL"],
            api_key=self.api_config["NEXT_API_KEY"],
        )
        self.name_mapping = name_mapping