from humantrace.datasets.downloader import HuggingFaceDownloader

from humantrace.datasets.config import (
    RAW_AI_DIR,
    RAW_HUMAN_DIR,
)

from humantrace.datasets.utils import (
    ensure_directory,
    print_header,
    save_jsonl,
)

TARGET = 500


def main():

    print_header("Downloading HC3")

    ensure_directory(RAW_HUMAN_DIR)
    ensure_directory(RAW_AI_DIR)

    downloader = HuggingFaceDownloader(

        dataset="Hello-SimpleAI/HC3",

        config="all",

        chunk_size=100,

    )

    rows = downloader.download()

    human = []

    ai = []

    for item in rows:

        record = item["row"]

        human_answers = record.get(
            "human_answers",
            [],
        )

        ai_answers = record.get(
            "chatgpt_answers",
            [],
        )

        for answer in human_answers:

            human.append({

                "text": answer,

                "label": "human",

                "dataset": "HC3",

            })

            if len(human) >= TARGET:
                break

        for answer in ai_answers:

            ai.append({

                "text": answer,

                "label": "ai",

                "dataset": "HC3",

            })

            if len(ai) >= TARGET:
                break

        if len(human) >= TARGET and len(ai) >= TARGET:
            break

    save_jsonl(
        human,
        RAW_HUMAN_DIR / "hc3.jsonl",
    )

    save_jsonl(
        ai,
        RAW_AI_DIR / "hc3.jsonl",
    )

    print()

    print(f"Human essays : {len(human)}")

    print(f"AI essays    : {len(ai)}")


if __name__ == "__main__":
    main()