import math
import statistics

from humantrace.feature_engine.base import FeatureExtractor


class DistributionFeatures(FeatureExtractor):

    name = "burstiness_distribution"

    def _entropy(self, values):

        total = sum(values)

        if total == 0:
            return 0.0

        entropy = 0.0

        for value in values:

            if value <= 0:
                continue

            probability = value / total

            entropy -= (
                probability
                * math.log2(probability)
            )

        return entropy

    def extract(self, document):

        lengths = [
            len(sentence.split())
            for sentence in document.sentences
        ]

        if not lengths:
            return {
                "sentence_length_entropy": 0.0,
                "sentence_length_variance": 0.0,
            }

        return {

            "sentence_length_entropy":
                self._entropy(lengths),

            "sentence_length_variance":
                statistics.pvariance(lengths)
                if len(lengths) > 1
                else 0.0,
        }