from humantrace.feature_engine.base import FeatureExtractor


class RichnessFeatures(FeatureExtractor):

    name = "lexical_richness"

    def extract(self, document):

        words = [
            token
            for token in document.doc_tokens
            if token.is_alpha
        ]

        if not words:
            return {
                "lexical_density": 0.0,
                "content_word_ratio": 0.0,
                "function_word_ratio": 0.0,
            }

        content_words = [
            token
            for token in words
            if token.pos_ in {
                "NOUN",
                "VERB",
                "ADJ",
                "ADV",
                "PROPN"
            }
        ]

        content_ratio = (
            len(content_words) / len(words)
        )

        return {
            "lexical_density": content_ratio,

            "content_word_ratio": content_ratio,

            "function_word_ratio":
                1 - content_ratio,
        }