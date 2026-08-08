from humantrace.feature_engine.base import FeatureExtractor


class CapitalizationFeatures(FeatureExtractor):

    name = "stylometry_capitalization"

    def extract(self, document):

        words = [
            word
            for word in document.tokens
            if word.isalpha()
        ]

        if not words:
            return {
                "uppercase_ratio": 0.0,
                "all_caps_ratio": 0.0,
                "title_case_ratio": 0.0,
            }

        uppercase = sum(
            1 for word in words
            if word.isupper()
        )

        all_caps = sum(
            1
            for word in words
            if len(word) > 1 and word.isupper()
        )

        title_case = sum(
            1
            for word in words
            if word.istitle()
        )

        total = len(words)

        return {

            "uppercase_ratio":
                uppercase / total,

            "all_caps_ratio":
                all_caps / total,

            "title_case_ratio":
                title_case / total,
        }