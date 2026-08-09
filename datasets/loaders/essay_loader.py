import json
from pathlib import Path
from typing import Iterator, Dict, Any

from .base import DatasetLoader


class JSONLEssayLoader(DatasetLoader):

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> Iterator[Dict[str, Any]]:

        if not self.path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {self.path}"
            )

        with self.path.open(
            "r",
            encoding="utf-8"
        ) as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                try:
                    record = json.loads(line)

                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Invalid JSON on line {line_number}"
                    ) from exc

                yield record