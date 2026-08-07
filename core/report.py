from typing import Dict, Any

from pydantic import BaseModel, Field

from .enums import AnalysisStatus
from .prediction import PredictionResult


class AnalysisReport(BaseModel):

    status: AnalysisStatus = (
        AnalysisStatus.SUCCESS
    )


    prediction: PredictionResult


    feature_summary: Dict[
        str,
        float
    ] = Field(
        default_factory=dict
    )


    explanations: Dict[
        str,
        Any
    ] = Field(
        default_factory=dict
    )


    model_version: str = "v1.0"