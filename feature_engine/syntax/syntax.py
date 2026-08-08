from collections import Counter

from humantrace.feature_engine.base import FeatureExtractor


class SyntaxFeatures(FeatureExtractor):

    name = "syntax"

    def extract(self, document):

        tokens = document.doc_tokens

        if not tokens:
            return {}

        total = len(tokens)

        pos_counts = Counter(
            token.pos_
            for token in tokens
            if not token.is_space
        )

        def ratio(tag):
            return pos_counts[tag] / total

        dependency_depths = []

        for token in tokens:

            depth = 0
            current = token

            while current.head != current:

                depth += 1
                current = current.head

                if depth > 100:
                    break

            dependency_depths.append(depth)

        avg_depth = (
            sum(dependency_depths)
            / len(dependency_depths)
        )

        passive_count = sum(
            1
            for token in tokens
            if token.dep_ == "auxpass"
            or token.dep_ == "nsubjpass"
        )

        sentence_count = max(
            len(document.sentences),
            1
        )

        return {

            "noun_ratio": ratio("NOUN"),

            "verb_ratio": ratio("VERB"),

            "adjective_ratio": ratio("ADJ"),

            "adverb_ratio": ratio("ADV"),

            "pronoun_ratio": ratio("PRON"),

            "preposition_ratio": ratio("ADP"),

            "conjunction_ratio": ratio("CCONJ"),

            "determiner_ratio": ratio("DET"),

            "average_dependency_depth":
                avg_depth,

            "passive_voice_ratio":
                passive_count / sentence_count,
        }