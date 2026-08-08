from collections import Counter

from humantrace.feature_engine.base import FeatureExtractor


class NgramFeatures(FeatureExtractor):

    name = "repetition_ngrams"

    def _ngrams(self, words, n):

        return [
            tuple(words[i:i + n])
            for i in range(
                len(words) - n + 1
            )
        ]

    def _repetition_ratio(self, ngrams):

        if not ngrams:
            return 0.0

        counts = Counter(ngrams)

        repeated = sum(
            count - 1
            for count in counts.values()
            if count > 1
        )

        return repeated / len(ngrams)

    def extract(self, document):

        words = [
            word.lower()
            for word in document.tokens
            if word.isalpha()
        ]

        bigrams = self._ngrams(words, 2)
        trigrams = self._ngrams(words, 3)

        return {

            "bigram_repetition_ratio":
                self._repetition_ratio(bigrams),

            "trigram_repetition_ratio":
                self._repetition_ratio(trigrams),

            "bigram_unique_ratio":
                (
                    len(set(bigrams)) / len(bigrams)
                    if bigrams else 0.0
                ),

            "trigram_unique_ratio":
                (
                    len(set(trigrams)) / len(trigrams)
                    if trigrams else 0.0
                ),
        }