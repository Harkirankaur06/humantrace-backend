from humantrace.datasets.downloader import HuggingFaceDownloader
import json

downloader = HuggingFaceDownloader(
    dataset="Hello-SimpleAI/HC3",
    config="all",
    chunk_size=1
)

rows = downloader.download(limit=1)

record = rows[0]["row"]

print("=" * 80)
print(record.keys())
print("=" * 80)

for key, value in record.items():
    print(f"\n{key}")
    print(type(value))

    if isinstance(value, list):
        print(f"Length: {len(value)}")
        if len(value):
            print(value[0])

    else:
        print(value)