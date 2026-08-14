import json
from pathlib import Path

from datasets import load_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "raw"
    / "human"
    / "essays.jsonl"
)

print("Loading dataset...")

dataset = load_dataset(
    "trentmkelly/lots-of-essays",
    data_files="filtered.jsonl",
    split="train",
)

print(f"Loaded {len(dataset)} essays")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

count = 0

with OUTPUT_FILE.open("w", encoding="utf-8") as out:

    for sample in dataset:

        text = sample["text"].strip()

        if len(text) < 500:
            continue

        record = {
            "essay_id": f"essay_{count}",
            "text": text,
            "label": "human",
            "source": "ESSAYS"
        }

        out.write(
            json.dumps(record, ensure_ascii=False)
            + "\n"
        )

        count += 1

        if count >= 5000:
            break

print(f"\nSaved {count} essays")