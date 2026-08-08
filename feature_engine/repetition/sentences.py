from collections import Counter

from humantrace.feature_engine.base import FeatureExtractor


class SentenceRepetitionFeatures(FeatureExtractor):

    name = "repetition_sentences"

    def extract(self, document):

        sentences = [
            sentence.lower().strip()
            for sentence in document.sentences
        ]

        if not sentences:
            return {
                "duplicate_sentence_ratio": 0.0,
                "repeated_sentence_count": 0,
            }

        counts = Counter(sentences)

        repeated = sum(
            1
            for count in counts.values()
            if count > 1
        )

        return {

            "duplicate_sentence_ratio":
                repeated / len(sentences),

            "repeated_sentence_count":
                repeated,
        }