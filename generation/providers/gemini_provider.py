import os

from google import genai

from ..base import LLMProvider
from ..prompts import (
    SYSTEM_PROMPT,
    build_prompt
)


class GeminiProvider(LLMProvider):

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv(
                "GEMINI_API_KEY"
            )
        )

        self.model = "gemini-2.5-pro"

    def generate(
        self,
        topic: str
    ) -> str:

        prompt = (
            SYSTEM_PROMPT
            + "\n\n"
            + build_prompt(topic)
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text.strip()