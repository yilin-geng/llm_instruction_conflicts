import time
import traceback
from openai import OpenAI
from .base import MODEL_LIST, BaseClient

models = list(filter(lambda x: x.startswith("gpt") or x.startswith("o"), MODEL_LIST))
name_mapping = {i:i for i in models}


class OpenAI_Client(BaseClient):
    def __init__(
        self,
        model: str = "gpt-4-turbo",
        api_config: dict = None,
        max_requests_per_minute=200,
        request_window=60,
    ):
        super().__init__(model, api_config, max_requests_per_minute, request_window)
        self.client_name = "OpenAI"
        assert self.api_config["OPENAI_API_KEY"] != ""
        self.client = OpenAI(api_key=self.api_config["OPENAI_API_KEY"])
        self.name_mapping = name_mapping

    def _call(self, messages: str, **kwargs):
        seed = kwargs.get("seed", 42)  # default seed is 42
        assert type(seed) is int, "Seed must be an integer."

        # Convert system role to developer if needed
        if self.system_role_name == "developer":
            for msg in messages:
                if msg["role"] == "system":
                    msg["role"] = "developer"

        num_retries = kwargs.get("num_retries", 1)
        post_check_function = kwargs.get("post_check_function", None)
        response_format = kwargs.get("response_format", None)  # JSON mode: response_format={ "type": "json_object" },

        r = ""

        for i in range(num_retries):
            try:
                response = self.client.chat.completions.create(
                    response_format=response_format,
                    seed=seed,
                    model=self.name_mapping[self.model],
                    messages=messages,
                )
                r = response.choices[0].message.content
                if post_check_function is None:
                    break
                else:
                    post_r = post_check_function(r)
                    if post_r:
                        return post_r
                    else:
                        print(f"Warning: Post check function failed. Response is {r}. Retrying {i} ...")
            except Exception as e:
                print("Error in LLM Client: ")
                print(traceback.format_exc())  # This will print the full stack trace
                time.sleep(1)      

        if r == "":
            print(f"{self.client_name} Client Warning: Empty response from LLM Client call.")
        
        return r

    def _log_usage(self, usage_dict):
        try:
            self.usage.prompt_tokens += usage_dict.prompt_tokens
            self.usage.completion_tokens += usage_dict.completion_tokens
        except:  # noqa E722
            print("Warning: prompt_tokens or completion_token not found in usage_dict")


    def construct_message_list(
        self,
        prompt_list: list[str],
        system_role: str = "You are a helpful assistant designed to output JSON.",
    ):
        messages_list = list()
        for prompt in prompt_list:
            messages = [
                {"role": self.system_role_name, "content": system_role},
                {"role": "user", "content": prompt},
            ]
            messages_list.append(messages)
        return messages_list