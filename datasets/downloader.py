from __future__ import annotations

import time
from typing import Dict, List
import time

import requests


BASE_URL = "https://datasets-server.huggingface.co/rows"


class HuggingFaceDownloader:
    """
    Generic downloader for HuggingFace Dataset Server.
    """

    def __init__(
        self,
        dataset: str,
        config: str,
        split: str = "train",
        chunk_size: int = 100,
        timeout: int = 60,
        delay: float = 0.25,
    ):

        self.dataset = dataset
        self.config = config
        self.split = split
        self.chunk_size = chunk_size
        self.timeout = timeout
        self.delay = delay


    def fetch_chunk(
        self,
        offset: int,
    ):

        params = {

            "dataset": self.dataset,

            "config": self.config,

            "split": self.split,

            "offset": offset,

            "length": self.chunk_size,

        }

        retries = 6

        wait = 2

        for attempt in range(retries):

            try:

                response = requests.get(

                    BASE_URL,

                    params=params,

                    timeout=self.timeout,

                )

                if response.status_code == 429:

                    print(
                        f"Rate limited. Waiting {wait} seconds..."
                    )

                    time.sleep(wait)

                    wait *= 2

                    continue

                response.raise_for_status()

                return response.json()["rows"]

            except requests.RequestException as e:

                print(e)

                print(f"Retry {attempt+1}/{retries}")

                time.sleep(wait)

                wait *= 2

        raise RuntimeError(
            f"Failed downloading offset {offset}"
        )

    def download(
        self,
        limit: int | None = None,
    ) -> List[Dict]:

        rows = []

        offset = 0

        while True:

            print(f"Downloading offset {offset}")

            chunk = self.fetch_chunk(offset)

            if len(chunk) == 0:
                break

            rows.extend(chunk)

            offset += self.chunk_size

            if limit is not None and len(rows) >= limit:
                rows = rows[:limit]
                break

            time.sleep(1)

        return rows