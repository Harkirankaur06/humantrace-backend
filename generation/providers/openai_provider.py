import os

from openai import OpenAI

from ..base import LLMProvider
from ..prompts import (
    SYSTEM_PROMPT,
    build_prompt
)


class OpenAIProvider(
    LLMProvider
):

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv(
                "OPENAI_API_KEY"
            )
        )

    def generate(
        self,
        topic: str
    ) -> str:

        response = self.client.chat.completions.create(

            model="gpt-4o",

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": build_prompt(topic)
                }
            ],

            temperature=1.0
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )