import json
import uuid
from pathlib import Path

from datasets import load_dataset

dataset = load_dataset(
    "ChristophSchuhmann/essays-with-instructions",
    split="train"
)

OUTPUT = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "raw"
    / "human"
    / "essays.jsonl"
)

with open(OUTPUT, "w", encoding="utf-8") as f:

    for sample in dataset:

        text = sample.get("essay", "").strip()

        if len(text) < 300:
            continue

        record = {
            "essay_id": f"essay_{uuid.uuid4().hex}",
            "text": text,
            "label": "human",
            "source": "essay",
        }

        f.write(
            json.dumps(record, ensure_ascii=False)
            + "\n"
        )