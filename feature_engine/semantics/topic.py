from collections import Counter

from humantrace.feature_engine.base import FeatureExtractor


class TopicFeatures(FeatureExtractor):

    name = "semantics_topic"

    def extract(self, document):

        words = [
            word.lower()
            for word in document.tokens
            if word.isalpha()
        ]

        if not words:
            return {
                "content_word_diversity": 0.0,
            }

        content_words = [
            token
            for token in document.doc_tokens
            if token.is_alpha
            and token.pos_ in {
                "NOUN",
                "PROPN",
                "VERB",
                "ADJ"
            }
        ]

        unique_content = len(
            set(
                token.lemma_.lower()
                for token in content_words
            )
        )

        return {
            "content_word_diversity":
                unique_content
                / max(len(content_words), 1)
        }