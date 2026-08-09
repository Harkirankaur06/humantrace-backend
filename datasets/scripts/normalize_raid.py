import json
import sys
from pathlib import Path


# Allow imports when running this file directly
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from datasets.loaders.essay_loader import JSONLEssayLoader
from datasets.validation.validator import validate_record


RAW_DIR = PROJECT_ROOT / "datasets" / "raw" / "ai"
OUTPUT_DIR = PROJECT_ROOT / "datasets" / "processed"

OUTPUT_FILE = OUTPUT_DIR / "raid_normalized.jsonl"


def normalize_record(record: dict, index: int) -> dict:
    text = record["text"].strip()

    normalized = {
        "essay_id": f"raid_{index:07d}",
        "text": text,
        "label": "ai",
        "source": "RAID",
    }

    validate_record(normalized)

    return normalized


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    input_files = list(RAW_DIR.glob("*.jsonl"))

    if not input_files:
        raise FileNotFoundError(
            f"No JSONL files found in {RAW_DIR}"
        )

    total = 0

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as output:

        for input_file in input_files:

            print(f"Processing: {input_file.name}")

            loader = JSONLEssayLoader(input_file)

            for index, record in enumerate(
                loader.load(),
                start=1
            ):
                normalized = normalize_record(
                    record,
                    total + 1
                )

                output.write(
                    json.dumps(
                        normalized,
                        ensure_ascii=False
                    )
                    + "\n"
                )

                total += 1

    print()
    print("RAID normalization complete.")
    print(f"Records: {total}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()