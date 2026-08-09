from humantrace.datasets.downloader import HuggingFaceDownloader

from humantrace.datasets.config import RAW_AI_DIR

from humantrace.datasets.utils import (
    ensure_directory,
    print_header,
    save_jsonl,
)

TARGET = 1000


def main():

    print_header("Downloading RAID")

    ensure_directory(RAW_AI_DIR)

    downloader = HuggingFaceDownloader(

        dataset="liamdugan/raid",

        config="raid",

        chunk_size=100,

    )

    rows = downloader.download(limit=TARGET)

    essays = []

    for item in rows:

        record = item["row"]

        text = record.get("generation")

        if not text:
            continue

        essays.append({

            "text": text,

            "label": "ai",

            "dataset": "RAID",

            "model": record.get("model"),

            "attack": record.get("attack"),

        })

    save_jsonl(
        essays,
        RAW_AI_DIR / "raid.jsonl",
    )

    print()

    print(f"Downloaded {len(essays)} RAID essays")


if __name__ == "__main__":
    main()