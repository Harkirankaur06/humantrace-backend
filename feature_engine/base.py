from abc import ABC, abstractmethod
from typing import Dict, Any


class FeatureExtractor(ABC):
    """
    Base interface for all HumanTrace feature extractors.
    """

    name: str = "base"

    @abstractmethod
    def extract(self, document) -> Dict[str, Any]:
        """
        Extract features from an EssayDocument.
        """
        raise NotImplementedError