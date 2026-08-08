from humantrace.feature_engine.base import FeatureExtractor


class CohesionFeatures(FeatureExtractor):

    name = "semantics_cohesion"

    def extract(self, document):

        sentences = document.sentences

        if len(sentences) < 2:
            return {
                "sentence_length_continuity": 0.0,
            }

        lengths = [
            len(sentence.split())
            for sentence in sentences
        ]

        differences = [
            abs(lengths[i] - lengths[i - 1])
            for i in range(1, len(lengths))
        ]

        average_difference = (
            sum(differences)
            / len(differences)
        )

        return {
            "sentence_length_continuity":
                1 / (1 + average_difference)
        }