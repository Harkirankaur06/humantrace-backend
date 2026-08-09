import json
import random
import sys
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from datasets.validation.validator import validate_record


INPUT_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "humantrace_dataset.jsonl"
)

SPLIT_DIR = (
    PROJECT_ROOT
    / "datasets"
    / "splits"
)

SEED = 42

TRAIN_RATIO = 0.80
VAL_RATIO = 0.10
TEST_RATIO = 0.10


def load_records():

    records = []

    with INPUT_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            record = json.loads(line)

            validate_record(record)

            records.append(record)

    return records


def split_records(records):

    grouped = defaultdict(list)

    for record in records:
        grouped[
            record["label"]
        ].append(record)

    train = []
    validation = []
    test = []

    random.seed(SEED)

    for label, items in grouped.items():

        random.shuffle(items)

        total = len(items)

        train_end = int(
            total * TRAIN_RATIO
        )

        val_end = train_end + int(
            total * VAL_RATIO
        )

        train.extend(
            items[:train_end]
        )

        validation.extend(
            items[train_end:val_end]
        )

        test.extend(
            items[val_end:]
        )

        print(
            f"{label}: "
            f"{len(items)} total → "
            f"{len(items[:train_end])} train, "
            f"{len(items[train_end:val_end])} val, "
            f"{len(items[val_end:])} test"
        )

    random.shuffle(train)
    random.shuffle(validation)
    random.shuffle(test)

    return train, validation, test


def write_jsonl(
    records,
    path: Path
):

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:

        for record in records:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )


def main():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}"
        )

    SPLIT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    records = load_records()

    print(
        f"Loaded {len(records)} records."
    )

    train, validation, test = split_records(
        records
    )

    write_jsonl(
        train,
        SPLIT_DIR / "train.jsonl"
    )

    write_jsonl(
        validation,
        SPLIT_DIR / "validation.jsonl"
    )

    write_jsonl(
        test,
        SPLIT_DIR / "test.jsonl"
    )

    print()
    print("Dataset splitting complete.")
    print(
        f"Train: {len(train)}"
    )
    print(
        f"Validation: {len(validation)}"
    )
    print(
        f"Test: {len(test)}"
    )


if __name__ == "__main__":
    main()