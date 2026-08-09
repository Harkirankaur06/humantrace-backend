import json
import uuid
from pathlib import Path


def ensure_directory(path: Path):

    path.mkdir(
        parents=True,
        exist_ok=True
    )


def generate_id(prefix: str):

    return f"{prefix}_{uuid.uuid4().hex}"


def save_jsonl(
        records,
        filepath: Path
):

    ensure_directory(filepath.parent)

    with filepath.open(
            "w",
            encoding="utf-8"
    ) as f:

        for record in records:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
            )

            f.write("\n")


def load_jsonl(
        filepath: Path
):

    with filepath.open(
            encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if line:

                yield json.loads(line)


def save_json(
        data,
        filepath: Path
):

    ensure_directory(filepath.parent)

    with filepath.open(
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def load_json(
        filepath: Path
):

    with filepath.open(
            encoding="utf-8"
    ) as f:

        return json.load(f)


def count_words(text: str):

    return len(text.split())


def count_sentences(text: str):

    return text.count(".") + text.count("?") + text.count("!")


def count_characters(text: str):

    return len(text)


def print_header(title: str):

    print("=" * 60)

    print(title)

    print("=" * 60)