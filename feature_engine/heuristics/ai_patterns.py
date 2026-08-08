import re

from humantrace.feature_engine.base import FeatureExtractor


class AIPatternFeatures(FeatureExtractor):

    name = "heuristic_ai_patterns"

    PATTERNS = [
        r"\bin today's (?:rapidly )?changing world\b",
        r"\bit is important to note\b",
        r"\bplays a crucial role\b",
        r"\bin conclusion\b",
        r"\bfurthermore\b",
        r"\bmoreover\b",
        r"\bdelve into\b",
        r"\bcomprehensive\b",
    ]

    def extract(self, document):

        text = document.clean_text.lower()

        matches = 0

        for pattern in self.PATTERNS:

            matches += len(
                re.findall(
                    pattern,
                    text
                )
            )

        word_count = max(
            len(document.tokens),
            1
        )

        return {

            "ai_pattern_count":
                matches,

            "ai_pattern_density":
                matches / word_count,
        }