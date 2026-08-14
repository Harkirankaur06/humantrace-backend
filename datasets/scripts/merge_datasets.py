import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from datasets.validation.validator import validate_record


PROCESSED_DIR = PROJECT_ROOT / "datasets" / "processed"

OUTPUT_FILE = (
    PROCESSED_DIR / "humantrace_dataset.jsonl"
)


INPUT_FILES = [
    PROCESSED_DIR / "raid_normalized.jsonl",
    PROCESSED_DIR / "hc3_ai_normalized.jsonl",
    PROCESSED_DIR / "hc3_human_normalized.jsonl",
    PROCESSED_DIR / "wikipedia_normalized.jsonl",
]


def read_records(path: Path):

    if not path.exists():
        raise FileNotFoundError(
            f"Missing normalized dataset: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1
        ):

            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {path} "
                    f"line {line_number}"
                ) from exc

            validate_record(record)

            yield record


def main():

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    total = 0

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as output:

        for input_file in INPUT_FILES:

            print(
                f"Merging: {input_file.name}"
            )

            for record in read_records(
                input_file
            ):

                output.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    )
                    + "\n"
                )

                total += 1

    print()
    print("Dataset merge complete.")
    print(f"Total records: {total}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()