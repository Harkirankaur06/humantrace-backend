from abc import ABC, abstractmethod
from typing import Iterator, Dict, Any


class DatasetLoader(ABC):

    @abstractmethod
    def load(self) -> Iterator[Dict[str, Any]]:
        """
        Load dataset records one at a time.
        """
        raise NotImplementedError