from typing import Dict, List, Any

from pydantic import BaseModel, Field

from .enums import (
    PredictionLabel,
    ConfidenceLevel
)


class SentencePrediction(BaseModel):

    sentence_index: int

    sentence_text: str

    probability: float

    label: PredictionLabel


class PredictionResult(BaseModel):

    label: PredictionLabel

    probability: float

    confidence: ConfidenceLevel


    sentence_predictions: List[
        SentencePrediction
    ] = Field(
        default_factory=list
    )


    important_features: Dict[
        str,
        float
    ] = Field(
        default_factory=dict
    )


    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )