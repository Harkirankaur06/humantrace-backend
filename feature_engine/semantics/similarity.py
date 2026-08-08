from humantrace.feature_engine.base import FeatureExtractor


class SimilarityFeatures(FeatureExtractor):

    name = "semantics_similarity"

    def _jaccard(self, a, b):

        a = set(a)
        b = set(b)

        union = a | b

        if not union:
            return 0.0

        return len(a & b) / len(union)

    def extract(self, document):

        sentences = document.sentences

        similarities = []

        for i in range(1, len(sentences)):

            previous = sentences[i - 1].lower().split()
            current = sentences[i].lower().split()

            similarities.append(
                self._jaccard(
                    previous,
                    current
                )
            )

        if not similarities:
            return {
                "adjacent_sentence_similarity": 0.0,
            }

        return {
            "adjacent_sentence_similarity":
                sum(similarities)
                / len(similarities)
        }