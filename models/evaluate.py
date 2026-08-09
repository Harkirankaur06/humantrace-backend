import json
from pathlib import Path

import numpy as np
import torch

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TEST_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "splits"
    / "test.jsonl"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "models"
    / "saved"
    / "humantrace-distilbert"
)


MAX_LENGTH = 512


# ============================================================
# LOAD DATA
# ============================================================

def load_records():

    records = []

    with TEST_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            records.append(
                json.loads(line)
            )

    return records


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("HumanTrace Model Evaluation")
    print("=" * 60)

    if not MODEL_DIR.exists():

        raise FileNotFoundError(
            "Trained model not found.\n"
            "Run train.py first."
        )

    records = load_records()

    print(
        f"\nTest records: {len(records)}"
    )

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    tokenizer = (
        AutoTokenizer.from_pretrained(
            str(MODEL_DIR)
        )
    )

    model = (
        AutoModelForSequenceClassification
        .from_pretrained(
            str(MODEL_DIR)
        )
    )

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    model.to(device)

    model.eval()

    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    y_true = []

    y_pred = []

    probabilities = []

    print(
        "\nRunning predictions..."
    )

    with torch.no_grad():

        for record in records:

            encoding = tokenizer(
                record["text"],
                truncation=True,
                padding=True,
                max_length=MAX_LENGTH,
                return_tensors="pt"
            )

            encoding = {
                key: value.to(device)
                for key, value in encoding.items()
            }

            outputs = model(
                **encoding
            )

            probs = torch.softmax(
                outputs.logits,
                dim=-1
            )

            prediction = torch.argmax(
                probs,
                dim=-1
            ).item()

            ai_probability = (
                probs[0][1].item()
            )

            true_label = (
                0
                if record["label"] == "human"
                else 1
            )

            y_true.append(
                true_label
            )

            y_pred.append(
                prediction
            )

            probabilities.append(
                ai_probability
            )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    matrix = confusion_matrix(
        y_true,
        y_pred
    )

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print("RESULTS")

    print("=" * 60)

    print(
        f"\nAccuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1 Score : {f1:.4f}"
    )

    print(
        "\nConfusion Matrix:"
    )

    print(matrix)

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_true,
            y_pred,
            target_names=[
                "human",
                "ai"
            ],
            zero_division=0
        )
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":
    main()