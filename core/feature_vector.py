from typing import Dict, Any
from pydantic import BaseModel, Field


class FeatureVector(BaseModel):
    """
    Numerical representation of an essay.
    Input for ML models.
    """


    features: Dict[str, float] = Field(
        default_factory=dict
    )


    version: str = "1.0"


    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


    def add_feature(
        self,
        name: str,
        value: float
    ):
        self.features[name] = value


    def get_feature(
        self,
        name: str
    ):
        return self.features.get(name)


    def count(self):
        return len(self.features)