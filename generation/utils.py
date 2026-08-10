import json

from pathlib import Path


def load_topics(path):

    with open(
        path,
        encoding="utf8"
    ) as file:

        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def already_generated(path):

    path = Path(path)

    if not path.exists():

        return set()

    topics = set()

    with path.open(
        encoding="utf8"
    ) as file:

        for line in file:

            record = json.loads(
                line
            )

            topics.add(
                record["topic"]
            )

    return topics


def append_jsonl(
    path,
    record
):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with path.open(
        "a",
        encoding="utf8"
    ) as file:

        json.dump(
            record,
            file,
            ensure_ascii=False
        )

        file.write(
            "\n"
        )