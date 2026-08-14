import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = (
    PROJECT_ROOT
    / "datasets"
    / "raw"
    / "human"
    / "bawe"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "raw"
    / "human"
    / "bawe.jsonl"
)


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


with OUTPUT_FILE.open("w", encoding="utf-8") as out:

    essay_id = 0

    for xml_file in INPUT_DIR.rglob("*.xml"):

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            text = " ".join(root.itertext())
            text = clean(text)

            if len(text) < 500:
                continue

            record = {
                "essay_id": f"bawe_{essay_id}",
                "text": text,
                "label": "human",
                "source": "BAWE",
            }

            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            essay_id += 1

        except Exception:
            continue

print(f"Saved {essay_id} essays to {OUTPUT_FILE}")