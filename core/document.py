from datetime import datetime
from typing import List, Dict, Any

from pydantic import BaseModel, Field


class EssayDocument(BaseModel):
    """
    Internal representation of an essay.

    Created after preprocessing.
    """


    raw_text: str = Field(
        description="Original user input"
    )


    clean_text: str = Field(
        default="",
        description="Normalized text after cleaning"
    )


    paragraphs: List[str] = Field(
        default_factory=list
    )


    sentences: List[str] = Field(
        default_factory=list
    )


    tokens: List[str] = Field(
        default_factory=list
    )


    lemmas: List[str] = Field(
        default_factory=list
    )


    pos_tags: List[str] = Field(
        default_factory=list
    )


    dependencies: List[str] = Field(
        default_factory=list
    )


    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


    @property
    def word_count(self) -> int:
        return len(self.tokens)


    @property
    def sentence_count(self) -> int:
        return len(self.sentences)