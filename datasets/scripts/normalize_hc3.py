import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from datasets.loaders.essay_loader import JSONLEssayLoader
from datasets.validation.validator import validate_record


RAW_AI_DIR = PROJECT_ROOT / "datasets" / "raw" / "ai"
RAW_HUMAN_DIR = PROJECT_ROOT / "datasets" / "raw" / "human"

OUTPUT_DIR = PROJECT_ROOT / "datasets" / "processed"

AI_OUTPUT = OUTPUT_DIR / "hc3_ai_normalized.jsonl"
HUMAN_OUTPUT = OUTPUT_DIR / "hc3_human_normalized.jsonl"


def normalize_record(
    record: dict,
    index: int,
    label: str
) -> dict:

    normalized = {
        "essay_id": f"hc3_{label}_{index:07d}",
        "text": record["text"].strip(),
        "label": label,
        "source": "HC3",
    }

    validate_record(normalized)

    return normalized


def process_directory(
    directory: Path,
    output_file: Path,
    label: str
):

    input_files = list(directory.glob("*.jsonl"))

    if not input_files:
        raise FileNotFoundError(
            f"No JSONL files found in {directory}"
        )

    count = 0

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as output:

        for input_file in input_files:

            print(
                f"Processing {label}: "
                f"{input_file.name}"
            )

            loader = JSONLEssayLoader(input_file)

            for record in loader.load():

                count += 1

                normalized = normalize_record(
                    record,
                    count,
                    label
                )

                output.write(
                    json.dumps(
                        normalized,
                        ensure_ascii=False
                    )
                    + "\n"
                )

    return count


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    ai_count = process_directory(
        RAW_AI_DIR,
        AI_OUTPUT,
        "ai"
    )

    human_count = process_directory(
        RAW_HUMAN_DIR,
        HUMAN_OUTPUT,
        "human"
    )

    print()
    print("HC3 normalization complete.")
    print(f"AI records: {ai_count}")
    print(f"Human records: {human_count}")
    print(f"AI output: {AI_OUTPUT}")
    print(f"Human output: {HUMAN_OUTPUT}")


if __name__ == "__main__":
    main()