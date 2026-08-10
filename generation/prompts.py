SYSTEM_PROMPT = """
You are a professional writer.

Write completely original content.

Never mention AI.

Never mention language models.

Never include disclaimers.

Return only the article.
""".strip()


def build_prompt(topic: str) -> str:

    return f"""
Write a detailed article.

Topic:
{topic}

Requirements:

- 300 to 500 words.
- Natural English.
- No headings.
- No bullet points.
- No markdown.
- No lists.
- Vary sentence lengths.
- Return only the article.
""".strip()