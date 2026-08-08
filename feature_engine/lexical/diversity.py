from collections import Counter

from humantrace.feature_engine.base import FeatureExtractor


class DiversityFeatures(FeatureExtractor):

    name = "lexical_diversity"

    def extract(self, document):

        words = [
            token.lower()
            for token in document.tokens
            if token.isalpha()
        ]

        total = len(words)

        if total == 0:
            return {
                "type_token_ratio": 0.0,
                "unique_word_ratio": 0.0,
                "hapax_ratio": 0.0,
                "repeated_word_ratio": 0.0,
            }

        counts = Counter(words)

        unique = len(counts)

        hapax = sum(
            1
            for count in counts.values()
            if count == 1
        )

        return {
            "type_token_ratio": unique / total,

            "unique_word_ratio": unique / total,

            "hapax_ratio": hapax / total,

            "repeated_word_ratio":
                1 - (unique / total),
        }