from collections import Counter

from humantrace.feature_engine.base import FeatureExtractor


class PunctuationFeatures(FeatureExtractor):

    name = "stylometry_punctuation"

    def extract(self, document):

        text = document.clean_text

        total_chars = max(len(text), 1)
        sentence_count = max(
            len(document.sentences),
            1
        )

        counts = Counter(text)

        return {

            "comma_frequency":
                counts[","] / total_chars,

            "semicolon_frequency":
                counts[";"] / total_chars,

            "colon_frequency":
                counts[":"] / total_chars,

            "dash_frequency":
                (
                    counts["-"]
                    + counts["–"]
                    + counts["—"]
                ) / total_chars,

            "question_frequency":
                counts["?"] / sentence_count,

            "exclamation_frequency":
                counts["!"] / sentence_count,

            "quotation_frequency":
                (
                    counts['"']
                    + counts["'"]
                ) / total_chars,

            "parenthesis_frequency":
                (
                    counts["("]
                    + counts[")"]
                ) / total_chars,
        }