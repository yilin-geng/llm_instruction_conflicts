import google
import google.auth
import google.auth.transport.requests
import openai
from openai import OpenAI
from .openai_client import OpenAI_Client

support_models = {"gemini-1.5-pro":"google/gemini-1.5-pro",
                  "gemini-1.0-pro":"google/gemini-1.0-pro",}


class Vertex_Client(OpenAI_Client):
    def __init__(
        self,
        model: str = "gemini-1.5-pro",
        api_config: dict = None,
        max_requests_per_minute=30,
        request_window=40,
    ):
        super().__init__(model, api_config, max_requests_per_minute, request_window)
        self.client_name = "Vertex"

        creds, project = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        # Note: the credential lives for 1 hour by default (https://cloud.google.com/docs/authentication/token-types#at-lifetime); after expiration, it must be refreshed.

        # Pass the Vertex endpoint and authentication to the OpenAI SDK
        PROJECT = "librai-411513"
        self.client = openai.OpenAI(
            base_url=f"https://us-central1-aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/us-central1/endpoints/openapi",
            api_key=creds.token,
        )
        self.support_models = support_models
