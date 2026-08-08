import math

import torch

from humantrace.feature_engine.base import FeatureExtractor
from humantrace.feature_engine.perplexity.model import (
    get_language_model
)


class PerplexityFeatures(FeatureExtractor):

    name = "perplexity"

    def extract(self, document):

        text = document.clean_text

        if not text.strip():
            return {
                "perplexity": 0.0,
            }

        tokenizer, model = get_language_model()

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )

        with torch.no_grad():

            outputs = model(
                **inputs,
                labels=inputs["input_ids"]
            )

        loss = outputs.loss

        perplexity = math.exp(
            loss.item()
        )

        return {
            "perplexity":
                float(perplexity),
        }