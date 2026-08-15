import sys
from pathlib import Path

import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_ID = "harkirankaur/humantrace-distilbert"

MAX_LENGTH = 512


# ============================================================
# MODEL
# ============================================================

class HumanTracePredictor:

    def __init__(self):

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        print(
            f"Loading HumanTrace model "
            f"on {self.device}..."
        )

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                MODEL_ID
            )
        )

        self.model = (
            AutoModelForSequenceClassification
            .from_pretrained(
                MODEL_ID
            )
        )

        self.model.to(
            self.device
        )

        self.model.eval()

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    def predict(
        self,
        text: str
    ) -> dict:

        if not isinstance(
            text,
            str
        ):

            raise TypeError(
                "Text must be a string."
            )

        if not text.strip():

            raise ValueError(
                "Text cannot be empty."
            )

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding=True,
            max_length=MAX_LENGTH,
            return_tensors="pt"
        )

        encoding = {
            key: value.to(
                self.device
            )
            for key, value in encoding.items()
        }

        with torch.no_grad():

            outputs = self.model(
                **encoding
            )

            probabilities = torch.softmax(
                outputs.logits,
                dim=-1
            )[0]

        human_probability = (
            probabilities[0].item()
        )

        ai_probability = (
            probabilities[1].item()
        )

        prediction = (
            "ai"
            if ai_probability >= human_probability
            else "human"
        )

        confidence = max(
            ai_probability,
            human_probability
        )

        return {
            "prediction": prediction,
            "confidence": round(
                confidence,
                4
            ),
            "ai_probability": round(
                ai_probability,
                4
            ),
            "human_probability": round(
                human_probability,
                4
            ),
        }


# ============================================================
# CLI
# ============================================================

def main():

    predictor = HumanTracePredictor()

    print()
    print(
        "=" * 60
    )
    print(
        "HumanTrace Detector"
    )
    print(
        "Type 'exit' to quit."
    )
    print(
        "=" * 60
    )

    while True:

        print()

        text = input(
            "Enter text: "
        )

        if text.lower().strip() == "exit":
            break

        try:

            result = predictor.predict(
                text
            )

            print()

            print(
                f"Prediction : "
                f"{result['prediction']}"
            )

            print(
                f"Confidence : "
                f"{result['confidence']:.2%}"
            )

            print(
                f"AI score   : "
                f"{result['ai_probability']:.2%}"
            )

            print(
                f"Human score: "
                f"{result['human_probability']:.2%}"
            )

        except Exception as exc:

            print(
                f"Error: {exc}"
            )


if __name__ == "__main__":
    main()