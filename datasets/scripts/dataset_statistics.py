import json
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from datasets.validation.validator import validate_record


DATASET_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "humantrace_dataset.jsonl"
)


def main():

    if not DATASET_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_FILE}"
        )

    label_counts = Counter()
    source_counts = Counter()

    text_lengths = []

    total = 0

    with DATASET_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            record = json.loads(line)

            validate_record(record)

            total += 1

            label_counts[
                record["label"]
            ] += 1

            source_counts[
                record["source"]
            ] += 1

            text_lengths.append(
                len(record["text"])
            )

    print()
    print("=" * 50)
    print("HumanTrace Dataset Statistics")
    print("=" * 50)

    print(f"\nTotal records: {total}")

    print("\nLabels:")
    for label, count in label_counts.items():

        percentage = (
            count / total * 100
        )

        print(
            f"  {label:15} "
            f"{count:8} "
            f"({percentage:.2f}%)"
        )

    print("\nSources:")
    for source, count in source_counts.items():

        percentage = (
            count / total * 100
        )

        print(
            f"  {source:15} "
            f"{count:8} "
            f"({percentage:.2f}%)"
        )

    if text_lengths:

        print("\nText length:")
        print(
            f"  Minimum: {min(text_lengths)}"
        )
        print(
            f"  Maximum: {max(text_lengths)}"
        )
        print(
            f"  Average: "
            f"{sum(text_lengths) / len(text_lengths):.2f}"
        )

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()