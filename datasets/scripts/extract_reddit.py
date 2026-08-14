import json
from pathlib import Path

from datasets import load_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT = (
    PROJECT_ROOT
    / "datasets"
    / "raw"
    / "human"
    / "reddit.jsonl"
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

print("Downloading Reddit dataset...")

dataset = load_dataset(
    "sentence-transformers/reddit",
    split="train",
    streaming=True
)

count = 0

with OUTPUT.open("w", encoding="utf-8") as f:

    for row in dataset:

        text = row.get("text", "").strip()

        if len(text) < 250:
            continue

        if len(text) > 3000:
            text = text[:3000]

        record = {
            "essay_id": f"reddit_{count}",
            "text": text,
            "label": "human",
            "source": "reddit"
        }

        f.write(json.dumps(record, ensure_ascii=False) + "\n")

        count += 1

        if count >= 3000:
            break

print(f"Saved {count} Reddit samples.")
print(OUTPUT)