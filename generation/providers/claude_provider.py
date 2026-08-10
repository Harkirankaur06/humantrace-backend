import os

import anthropic

from ..base import LLMProvider
from ..prompts import (
    SYSTEM_PROMPT,
    build_prompt
)


class ClaudeProvider(LLMProvider):

    def __init__(self):

        self.client = anthropic.Anthropic(
            api_key=os.getenv(
                "ANTHROPIC_API_KEY"
            )
        )

        self.model = "claude-sonnet-4-0"

    def generate(
        self,
        topic: str
    ) -> str:

        response = self.client.messages.create(

            model=self.model,

            max_tokens=900,

            temperature=1.0,

            system=SYSTEM_PROMPT,

            messages=[
                {
                    "role": "user",
                    "content": build_prompt(topic)
                }
            ]
        )

        return (
            response.content[0]
            .text
            .strip()
        )