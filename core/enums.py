from enum import Enum


class PredictionLabel(str, Enum):
    HUMAN = "human"
    AI_GENERATED = "ai_generated"
    AI_ASSISTED = "ai_assisted"
    UNCERTAIN = "uncertain"


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AnalysisStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PROCESSING = "processing"