import time
import asyncio
from abc import abstractmethod
from functools import partial
from collections import deque

from typing import Dict, List, Any, Optional
from dataclasses import dataclass

MODEL_LIST = [
    # openai: https://platform.openai.com/docs/models
    "o3-mini-2025-01-31",
    "o1",
    "o1-2024-12-17",
    "o1-mini-2024-09-12",
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-05-13",
    "gpt-4o-mini-2024-07-18",
    "o1-preview-2024-09-12",
    "gpt-4-turbo-2024-04-09",
    "gpt-4-0125-preview",
    "gpt-4-1106-preview",
    "gpt-4-0613",
    "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0613",
    # anthropic: https://docs.anthropic.com/en/docs/about-claude/models
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    # meta
    "meta-llama/Llama-3.2-3B-Instruct",
    "meta-llama/Llama-3.2-1B-Instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.1-70B-Instruct",
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "meta-llama/Meta-Llama-3-70B-Instruct",
    "meta-llama/Llama-2-7b-chat-hf",
    "meta-llama/Llama-2-13b-chat-hf",
    "meta-llama/Llama-2-70b-chat-hf",
    "meta-llama/CodeLlama-70b-Instruct-hf",
    "meta-llama/CodeLlama-34b-Instruct-hf",
    "meta-llama/CodeLlama-13b-Instruct-hf",
    "meta-llama/CodeLlama-7b-Instruct-hf",
    # moonshot: https://platform.moonshot.cn/docs/pricing/chat#%E4%BA%A7%E5%93%81%E5%AE%9A%E4%BB%B7
    "moonshot-v1-8k",
    "moonshot-v1-32k",
    "moonshot-v1-128k",
    # mistral: https://docs.mistral.ai/getting-started/models/models_overview/#tag/batch/operation/jobs_api_routes_batch_cancel_batch_job
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "mistralai/Mistral-7B-Instruct-v0.1",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mistral-Nemo-Instruct-2407",
    # alibaba: https://huggingface.co/Qwen
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-32B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-3B-Instruct",
    "Qwen/Qwen2.5-1.5B-Instruct",
    "Qwen/Qwen2.5-0.5B-Instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "Qwen/Qwen2.5-Coder-14B-Instruct",
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    "Qwen/Qwen2.5-Coder-3B-Instruct",
    "Qwen/Qwen2.5-Coder-1.5B-Instruct",
    "Qwen/Qwen2.5-Coder-0.5B-Instruct",
    "Qwen/Qwen2.5-Coder-3B-Instruct",
    "Qwen/Qwen2.5-Math-72B-Instruct",
    "Qwen/Qwen2.5-Math-7B-Instruct",
    "Qwen/Qwen2.5-Math-1.5B-Instruct",
    "Qwen/Qwen2-72B-Instruct",
    "Qwen/Qwen2-7B-Instruct",
    "Qwen/Qwen2-1.5B-Instruct",
    "Qwen/Qwen2-0.5B-Instruct",
    "Qwen/Qwen2-Math-72B-Instruct",
    "Qwen/Qwen2-Math-7B-Instruct",
    "Qwen/Qwen2-Math-1.5B-Instruct",
    "Qwen/Qwen1.5-72B-Chat",
    "Qwen/Qwen1.5-32B-Chat",
    "Qwen/Qwen1.5-14B-Chat",
    "Qwen/Qwen1.5-7B-Chat",
    "Qwen/Qwen1.5-4B-Chat",
    "Qwen/Qwen1.5-1.8B-Chat",
    "Qwen/Qwen1.5-0.5B-Chat",
    "Qwen/Qwen-72B-Chat",
    "Qwen/Qwen-14B-Chat",
    "Qwen/Qwen-7B-Chat",
    # Qwen Commercial: https://www.alibabacloud.com/help/en/model-studio/developer-reference/use-qwen-by-calling-api?spm=a2c63.p38356.0.0.c03973b5ufdoJe
    "qwen-max",
    "qwen-plus",
    "qwen-turbo",
    # google: https://ai.google.dev/gemini-api/docs/models/gemini#gemini-1.5-pro
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.0-pro",
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
    "google/gemma-2-2b-it",
    # deepseek
    "deepseek-chat",
    "deepseek-ai/DeepSeek-R1",
    "deepseek-reasoner",
    "deepseek-ai/DeepSeek-V3",
    "deepseek-ai/DeepSeek-V2.5-1210",
    "deepseek-ai/DeepSeek-V2-Chat",
    "deepseek-ai/DeepSeek-V2-Lite-Chat",
    "deepseek-ai/DeepSeek-Coder-V2-Instruct",
    "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
    "deepseek-ai/deepseek-llm-67b-chat",
    "deepseek-ai/deepseek-llm-7b-chat",
    "deepseek-ai/deepseek-coder-33b-instruct",
    "deepseek-ai/deepseek-coder-6.7b-instruct",
    "deepseek-ai/deepseek-coder-1.3b-instruct",
    "deepseek-ai/deepseek-math-7b-instruct",
    # zhipu: https://bigmodel.cn/pricing
    "GLM-4-Plus",
    "GLM-4-0520",
    "GLM-4-Air",
    "GLM-4-Flash",
    # 01: https://platform.lingyiwanwu.com/docs#%E6%A8%A1%E5%9E%8B%E4%B8%8E%E8%AE%A1%E8%B4%B9
    "yi-lightning",
    "yi-large",
    "yi-medium",
    "yi-spark",
    # AllenAI
    "allenai/OLMo-7B-0724-Instruct-hf",
    "allenai/OLMo-2-1124-13B-Instruct",
    "allenai/OLMoE-1B-7B-0924-Instruct",
    # Databricks
    "databricks/dbrx-instruct",
    # TII
    "tiiuae/falcon-40b-instruct",
    "tiiuae/falcon-mamba-7b-instruct",
    # G42
    "inceptionai/jais-family-13b-chat",
    "inceptionai/jais-family-30b-8k-chat",
    "inceptionai/jais-adapted-7b-chat",
    "inceptionai/jais-30b-chat-v3",
    "LLM360/K2-Chat",
    # Xverse
    "xverse/XVERSE-65B-Chat",
    # IBM
    "ibm-granite/granite-3.0-8b-instruct",
    # THU
    "THUDM/chatglm3-6b",
    # Baichuan
    "baichuan-inc/Baichuan2-13B-Chat",
    "Llama-3.1-8B-Instruct-conflict",
]

@dataclass
class TokenUsage:
    model: str = ""
    prompt_tokens: int = 0
    completion_tokens: Optional[int] = 0


class BaseClient:
    # Models that use "developer" instead of "system"
    DEVELOPER_ROLE_MODELS = {
        "o1-2024-12-17",
        "o3-mini-2025-01-31",
        # Add other models that use "developer" role as needed
    }

    def __init__(
        self,
        model: str,
        api_config: dict,
        max_requests_per_minute: int,
        request_window: int,
    ) -> None:
        self.model = model
        self.api_config = api_config
        self.max_requests_per_minute = max_requests_per_minute
        self.request_window = request_window
        self.traffic_queue = deque()
        self.total_traffic = 0
        self.usage = TokenUsage(model=model)
        # Determine system role name based on model
        self.system_role_name = "developer" if model in self.DEVELOPER_ROLE_MODELS else "system"

    @abstractmethod
    def _call(self, messages: str):
        """Internal function to call the API."""
        pass

    @abstractmethod
    def _log_usage(self):
        """Log the usage of tokens, should be used in each client's _call method."""
        pass

    def get_usage(self):
        return self.usage

    def reset_usage(self):
        self.usage.prompt_tokens = 0
        self.usage.completion_tokens = 0

    @abstractmethod
    def construct_message_list(self, user_inputs: list[str], sys_inputs: list[str]) -> list[str]:
        """Construct a list of messages for the function self.multi_call."""
        raise NotImplementedError

    def get_request_length(self, messages):
        # TODO: check if we should return the len(menages) instead
        return 1

    def call(self, messages: list[str], num_retries=3, waiting_time=1, **kwargs):
        seed = kwargs.get("seed", 42)
        assert type(seed) is int, "Seed must be an integer."
        assert len(messages) == 1, "Only one message is allowed for this function."

        r = ""
        for _ in range(num_retries):
            try:
                r = self._call(messages[0], seed=seed)
                break
            except Exception as e:
                print(f"Error LLM Client call: {e} Retrying...")
                time.sleep(waiting_time)

        if r == "":
            raise ValueError("Failed to get response from LLM Client.")
        return r

    def set_model(self, model: str):
        self.model = model

    async def _async_call(self, messages: list, **kwargs):
        """Calls ChatGPT asynchronously, tracks traffic, and enforces rate limits."""
        while len(self.traffic_queue) >= self.max_requests_per_minute:
            await asyncio.sleep(1)
            self._expire_old_traffic()

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, partial(self._call, messages, **kwargs))

        self.total_traffic += self.get_request_length(messages)
        self.traffic_queue.append((time.time(), self.get_request_length(messages)))

        return response

    def multi_call(self, messages_list, **kwargs):
        tasks = [self._async_call(messages=messages, **kwargs) for messages in messages_list]
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        loop = asyncio.get_event_loop()
        responses = loop.run_until_complete(asyncio.gather(*tasks))
        return responses

    def _expire_old_traffic(self):
        """Expires traffic older than the request window."""
        current_time = time.time()
        while self.traffic_queue and self.traffic_queue[0][0] + self.request_window < current_time:
            self.total_traffic -= self.traffic_queue.popleft()[1]