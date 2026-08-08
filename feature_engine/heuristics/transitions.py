from humantrace.feature_engine.base import FeatureExtractor


class TransitionFeatures(FeatureExtractor):

    name = "heuristic_transitions"

    TRANSITIONS = {
        "furthermore",
        "moreover",
        "however",
        "therefore",
        "additionally",
        "consequently",
        "in conclusion",
        "on the other hand",
        "for example",
        "in addition",
    }

    def extract(self, document):

        text = document.clean_text.lower()

        count = 0

        matched = []

        for transition in self.TRANSITIONS:

            occurrences = text.count(
                transition
            )

            if occurrences:

                count += occurrences
                matched.append(transition)

        word_count = max(
            len(document.tokens),
            1
        )

        return {

            "transition_count":
                count,

            "transition_density":
                count / word_count,

            "transition_diversity":
                len(matched),
        }