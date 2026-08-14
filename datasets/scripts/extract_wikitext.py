import json
from pathlib import Path
from datasets import load_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT = (
    PROJECT_ROOT
    / "datasets"
    / "raw"
    / "human"
    / "wikitext.jsonl"
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

dataset = load_dataset(
    "wikitext",
    "wikitext-103-v1",
    split="train"
)

count = 0

with OUTPUT.open("w", encoding="utf-8") as f:

    for row in dataset:

        text = row["text"].strip()

        if len(text) < 300:
            continue

        if len(text) > 3000:
            text = text[:3000]

        record = {
            "essay_id": f"wiki_{count}",
            "text": text,
            "label": "human",
            "source": "WikiText"
        }

        f.write(json.dumps(record, ensure_ascii=False) + "\n")

        count += 1

print(f"Saved {count} samples.")