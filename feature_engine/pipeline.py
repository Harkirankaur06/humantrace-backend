from typing import Dict, Any

from humantrace.feature_engine.registry import FeatureRegistry

from humantrace.feature_engine.lexical.vocabulary import VocabularyFeatures
from humantrace.feature_engine.lexical.diversity import DiversityFeatures
from humantrace.feature_engine.lexical.richness import RichnessFeatures

from humantrace.feature_engine.readability.readability import ReadabilityFeatures

from humantrace.feature_engine.syntax.syntax import SyntaxFeatures

from humantrace.feature_engine.stylometry.punctuation import PunctuationFeatures
from humantrace.feature_engine.stylometry.capitalization import CapitalizationFeatures
from humantrace.feature_engine.stylometry.formatting import FormattingFeatures

from humantrace.feature_engine.repetition.ngrams import NgramFeatures
from humantrace.feature_engine.repetition.phrases import PhraseFeatures
from humantrace.feature_engine.repetition.sentences import SentenceRepetitionFeatures

from humantrace.feature_engine.burstiness.sentence_burstiness import SentenceBurstinessFeatures
from humantrace.feature_engine.burstiness.lexical_burstiness import LexicalBurstinessFeatures
from humantrace.feature_engine.burstiness.distribution import DistributionFeatures

from humantrace.feature_engine.semantics.cohesion import CohesionFeatures
from humantrace.feature_engine.semantics.similarity import SimilarityFeatures
from humantrace.feature_engine.semantics.topic import TopicFeatures

from humantrace.feature_engine.heuristics.ai_patterns import AIPatternFeatures
from humantrace.feature_engine.heuristics.transitions import TransitionFeatures
from humantrace.feature_engine.heuristics.templates import TemplateFeatures


def create_registry() -> FeatureRegistry:
    """
    Create the default HumanTrace feature registry.
    """

    registry = FeatureRegistry()

    extractors = [
        VocabularyFeatures(),
        DiversityFeatures(),
        RichnessFeatures(),

        ReadabilityFeatures(),

        SyntaxFeatures(),

        PunctuationFeatures(),
        CapitalizationFeatures(),
        FormattingFeatures(),

        NgramFeatures(),
        PhraseFeatures(),
        SentenceRepetitionFeatures(),

        SentenceBurstinessFeatures(),
        LexicalBurstinessFeatures(),
        DistributionFeatures(),

        CohesionFeatures(),
        SimilarityFeatures(),
        TopicFeatures(),

        AIPatternFeatures(),
        TransitionFeatures(),
        TemplateFeatures(),
    ]

    for extractor in extractors:
        registry.register(extractor)

    return registry


DEFAULT_REGISTRY = create_registry()


def extract_features(
    document,
    registry: FeatureRegistry = DEFAULT_REGISTRY
) -> Dict[str, Any]:
    """
    Extract all registered features from a document.
    """

    features = {}

    for extractor in registry.all():

        extracted = extractor.extract(document)

        for name, value in extracted.items():

            if name in features:
                raise ValueError(
                    f"Duplicate feature name detected: {name}"
                )

            features[name] = value

    return features