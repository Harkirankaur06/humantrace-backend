import re

from humantrace.feature_engine.base import FeatureExtractor


class TemplateFeatures(FeatureExtractor):

    name = "heuristic_templates"

    PATTERNS = [

        r"\bthere are several reasons why\b",

        r"\bone of the main reasons\b",

        r"\bthis essay will discuss\b",

        r"\bin this essay\b",

        r"\bfirst and foremost\b",

        r"\blast but not least\b",

        r"\bto summarize\b",

        r"\bto conclude\b",
    ]

    def extract(self, document):

        text = document.clean_text.lower()

        matches = []

        for pattern in self.PATTERNS:

            if re.search(
                pattern,
                text
            ):
                matches.append(pattern)

        return {

            "template_pattern_count":
                len(matches),

            "template_pattern_density":
                (
                    len(matches)
                    / max(
                        len(document.tokens),
                        1
                    )
                ),
        }