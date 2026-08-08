from humantrace.feature_engine.base import FeatureExtractor


class FormattingFeatures(FeatureExtractor):

    name = "stylometry_formatting"

    def extract(self, document):

        paragraphs = document.paragraphs

        if not paragraphs:
            return {
                "paragraph_count": 0,
                "average_paragraph_length": 0.0,
                "paragraph_length_std": 0.0,
            }

        lengths = [
            len(paragraph.split())
            for paragraph in paragraphs
        ]

        mean = sum(lengths) / len(lengths)

        variance = sum(
            (x - mean) ** 2
            for x in lengths
        ) / len(lengths)

        return {

            "paragraph_count":
                len(paragraphs),

            "average_paragraph_length":
                mean,

            "paragraph_length_std":
                variance ** 0.5,
        }