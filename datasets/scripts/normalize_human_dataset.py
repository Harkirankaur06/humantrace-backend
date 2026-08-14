import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FOLDER = (
    PROJECT_ROOT
    / "datasets"
    / "raw"
    / "human"
)

FILES = [
    "reddit.jsonl",
    "essays.jsonl",
    "wikipedia.jsonl",
]

def clean(text: str) -> str:

    text = text.replace("\r", " ")
    text = text.replace("\n", " ")

    text = re.sub(r"\[[0-9]+\]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


for filename in FILES:

    path = RAW_FOLDER / filename

    if not path.exists():
        continue

    output = path.with_name(
        path.stem + "_normalized.jsonl"
    )

    total = 0

    with (
        path.open("r", encoding="utf-8") as fin,
        output.open("w", encoding="utf-8") as fout,
    ):

        for line in fin:

            if not line.strip():
                continue

            record = json.loads(line)

            record["text"] = clean(record["text"])

            if len(record["text"]) < 200:
                continue

            fout.write(
                json.dumps(record, ensure_ascii=False)
                + "\n"
            )

            total += 1

    print(f"{filename} -> {total} records")

print("Done.")