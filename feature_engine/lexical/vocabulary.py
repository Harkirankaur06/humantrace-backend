import re
from collections import Counter

from humantrace.feature_engine.base import FeatureExtractor


class VocabularyFeatures(FeatureExtractor):

    name = "lexical_vocabulary"

    def extract(self, document):

        words = [
            token.lower()
            for token in document.tokens
            if re.search(r"[A-Za-z]", token)
        ]

        if not words:
            return {
                "word_count": 0,
                "unique_word_count": 0,
                "character_count": 0,
                "average_word_length": 0.0,
                "word_length_std": 0.0,
            }

        unique_words = set(words)

        word_lengths = [
            len(word)
            for word in words
        ]

        mean_length = sum(word_lengths) / len(word_lengths)

        variance = sum(
            (x - mean_length) ** 2
            for x in word_lengths
        ) / len(word_lengths)

        return {
            "word_count": len(words),

            "unique_word_count": len(unique_words),

            "character_count": len(document.clean_text),

            "average_word_length": mean_length,

            "word_length_std": variance ** 0.5,
        }