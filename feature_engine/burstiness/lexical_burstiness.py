import statistics
from collections import Counter

from humantrace.feature_engine.base import FeatureExtractor


class LexicalBurstinessFeatures(FeatureExtractor):

    name = "burstiness_lexical"

    def extract(self, document):

        words = [
            word.lower()
            for word in document.tokens
            if word.isalpha()
        ]

        if not words:
            return {
                "word_frequency_mean": 0.0,
                "word_frequency_std": 0.0,
                "word_frequency_cv": 0.0,
            }

        counts = Counter(words)

        frequencies = list(
            counts.values()
        )

        mean = statistics.mean(frequencies)

        std = (
            statistics.stdev(frequencies)
            if len(frequencies) > 1
            else 0.0
        )

        return {

            "word_frequency_mean":
                mean,

            "word_frequency_std":
                std,

            "word_frequency_cv":
                std / mean
                if mean else 0.0,
        }