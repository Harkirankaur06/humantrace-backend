from collections import Counter

from humantrace.feature_engine.base import FeatureExtractor


class PhraseFeatures(FeatureExtractor):

    name = "repetition_phrases"

    def extract(self, document):

        words = [
            word.lower()
            for word in document.tokens
            if word.isalpha()
        ]

        phrases = [
            tuple(words[i:i + 4])
            for i in range(
                len(words) - 3
            )
        ]

        counts = Counter(phrases)

        repeated_phrases = sum(
            1
            for count in counts.values()
            if count > 1
        )

        return {

            "repeated_four_word_phrases":
                repeated_phrases,

            "phrase_repetition_ratio":
                (
                    repeated_phrases / len(counts)
                    if counts else 0.0
                ),
        }