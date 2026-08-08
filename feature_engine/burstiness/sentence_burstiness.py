import statistics

from humantrace.feature_engine.base import FeatureExtractor


class SentenceBurstinessFeatures(FeatureExtractor):

    name = "burstiness_sentence"

    def extract(self, document):

        lengths = [
            len(sentence.split())
            for sentence in document.sentences
        ]

        if len(lengths) < 2:
            return {
                "sentence_length_mean": 0.0,
                "sentence_length_std": 0.0,
                "sentence_length_cv": 0.0,
            }

        mean = statistics.mean(lengths)
        std = statistics.stdev(lengths)

        return {

            "sentence_length_mean":
                mean,

            "sentence_length_std":
                std,

            "sentence_length_cv":
                std / mean if mean else 0.0,
        }