from typing import Dict, List

from humantrace.feature_engine.base import FeatureExtractor


class FeatureRegistry:
    """
    Registry containing all active feature extractors.
    """

    def __init__(self):
        self._extractors: Dict[str, FeatureExtractor] = {}

    def register(self, extractor: FeatureExtractor) -> None:
        """
        Register a feature extractor.
        """

        if extractor.name in self._extractors:
            raise ValueError(
                f"Feature extractor '{extractor.name}' "
                f"is already registered."
            )

        self._extractors[extractor.name] = extractor

    def get(self, name: str) -> FeatureExtractor:
        return self._extractors[name]

    def all(self) -> List[FeatureExtractor]:
        return list(self._extractors.values())

    def names(self) -> List[str]:
        return list(self._extractors.keys())

    def __len__(self):
        return len(self._extractors)