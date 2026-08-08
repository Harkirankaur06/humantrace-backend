import textstat

from humantrace.feature_engine.base import FeatureExtractor


class ReadabilityFeatures(FeatureExtractor):

    name = "readability"

    def extract(self, document):

        text = document.clean_text

        if not text.strip():
            return {
                "flesch_reading_ease": 0.0,
                "flesch_kincaid_grade": 0.0,
                "gunning_fog": 0.0,
                "smog_index": 0.0,
                "automated_readability_index": 0.0,
                "coleman_liau_index": 0.0,
            }

        return {
            "flesch_reading_ease":
                textstat.flesch_reading_ease(text),

            "flesch_kincaid_grade":
                textstat.flesch_kincaid_grade(text),

            "gunning_fog":
                textstat.gunning_fog(text),

            "smog_index":
                textstat.smog_index(text),

            "automated_readability_index":
                textstat.automated_readability_index(text),

            "coleman_liau_index":
                textstat.coleman_liau_index(text),
        }