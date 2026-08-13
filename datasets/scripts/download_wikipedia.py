import json
import uuid
from pathlib import Path

import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    user_agent="HumanTrace/1.0 (research project)",
    language="en",
)

TOPICS_FILE = (
    Path(__file__).resolve().parents[2]
    / "topics"
    / "topics.txt"
)

OUTPUT_FILE = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "raw"
    / "human"
    / "wikipedia.jsonl"
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

count = 0

with open(TOPICS_FILE, "r", encoding="utf-8") as topics, \
     open(OUTPUT_FILE, "a", encoding="utf-8") as out:

    for topic in topics:

        topic = topic.strip()

        if not topic:
            continue

        page = wiki.page(topic)

        if not page.exists():
            print(f"Skipped: {topic}")
            continue

        text = page.summary.strip()

        if len(text) < 300:
            continue

        record = {
            "essay_id": f"wiki_{uuid.uuid4().hex}",
            "text": text,
            "label": "human",
            "source": "wikipedia",
        }

        out.write(json.dumps(record, ensure_ascii=False) + "\n")

        count += 1
        print(f"{count}: {topic}")

print(f"\nFinished. Saved {count} records.")