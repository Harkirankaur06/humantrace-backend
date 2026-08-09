import json
import random
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRAIN_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "splits"
    / "train.jsonl"
)

VAL_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "splits"
    / "validation.jsonl"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "models"
    / "saved"
)

MODEL_NAME = "distilbert-base-uncased"

MAX_LENGTH = 512

SEED = 42


# ============================================================
# REPRODUCIBILITY
# ============================================================

def set_seed(seed=SEED):

    random.seed(seed)

    np.random.seed(seed)

    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ============================================================
# DATASET
# ============================================================

class HumanTraceDataset(Dataset):

    def __init__(
        self,
        path,
        tokenizer,
        max_length=MAX_LENGTH
    ):

        self.records = []

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                record = json.loads(line)

                self.records.append(record)

        self.tokenizer = tokenizer

        self.max_length = max_length

    def __len__(self):

        return len(self.records)

    def __getitem__(self, index):

        record = self.records[index]

        encoding = self.tokenizer(
            record["text"],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )

        item = {
            key: value.squeeze(0)
            for key, value in encoding.items()
        }

        if record["label"] == "human":
            label_id = 0

        elif record["label"] in {"ai", "ai_polished"}:
            label_id = 1

        else:
            raise ValueError(
                f"Unsupported label: {record['label']}"
            )

        item["labels"] = torch.tensor(
            label_id,
            dtype=torch.long
        )

        return item


# ============================================================
# LOAD RECORDS
# ============================================================

def prepare_file(path):

    records = []

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            record = json.loads(line)

            # Convert HumanTrace labels into integers.
            if record["label"] == "human":
                record["label_id"] = 0

            elif record["label"] in {
                "ai",
                "ai_polished"
            }:
                record["label_id"] = 1

            else:
                raise ValueError(
                    f"Unsupported label: "
                    f"{record['label']}"
                )

            records.append(record)

    return records


def save_prepared_file(records, path):

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:

        for record in records:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                )
                + "\n"
            )


# ============================================================
# METRICS
# ============================================================

def compute_metrics(eval_pred):

    predictions, labels = eval_pred

    predictions = np.argmax(
        predictions,
        axis=1
    )

    accuracy = (
        predictions == labels
    ).mean()

    return {
        "accuracy": float(accuracy)
    }


# ============================================================
# MAIN
# ============================================================

def main():

    set_seed()

    print("=" * 60)
    print("HumanTrace Model Training")
    print("=" * 60)

    print(
        f"\nModel: {MODEL_NAME}"
    )

    print(
        f"Train file: {TRAIN_FILE}"
    )

    print(
        f"Validation file: {VAL_FILE}"
    )

    # --------------------------------------------------------
    # Load and prepare data
    # --------------------------------------------------------

    train_records = prepare_file(
        TRAIN_FILE
    )

    val_records = prepare_file(
        VAL_FILE
    )

    print(
        f"\nTraining records: "
        f"{len(train_records)}"
    )

    print(
        f"Validation records: "
        f"{len(val_records)}"
    )

    # --------------------------------------------------------
    # Tokenizer
    # --------------------------------------------------------

    print(
        "\nLoading tokenizer..."
    )

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    # --------------------------------------------------------
    # Dataset
    # --------------------------------------------------------

    train_dataset = HumanTraceDataset(
        TRAIN_FILE,
        tokenizer
    )

    val_dataset = HumanTraceDataset(
        VAL_FILE,
        tokenizer
    )

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    print(
        "\nLoading model..."
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
        id2label={
            0: "human",
            1: "ai"
        },
        label2id={
            "human": 0,
            "ai": 1
        }
    )

    # --------------------------------------------------------
    # Training configuration
    # --------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    training_args = TrainingArguments(

        output_dir=str(
            MODEL_DIR / "checkpoints"
        ),

        eval_strategy="epoch",

        save_strategy="epoch",

        logging_strategy="steps",

        logging_steps=50,

        learning_rate=2e-5,

        per_device_train_batch_size=8,

        per_device_eval_batch_size=8,

        num_train_epochs=3,

        weight_decay=0.01,

        load_best_model_at_end=True,

        metric_for_best_model="accuracy",

        greater_is_better=True,

        save_total_limit=2,

        report_to="none",

        fp16=torch.cuda.is_available(),

        seed=SEED,
    )

    # --------------------------------------------------------
    # Trainer
    # --------------------------------------------------------

    trainer = Trainer(

        model=model,

        args=training_args,

        train_dataset=train_dataset,

        eval_dataset=val_dataset,

        processing_class=tokenizer,

        compute_metrics=compute_metrics,
    )

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    print(
        "\nStarting training..."
    )

    trainer.train()

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    final_model_dir = (
        MODEL_DIR / "humantrace-distilbert"
    )

    print(
        "\nSaving model..."
    )

    trainer.save_model(
        str(final_model_dir)
    )

    tokenizer.save_pretrained(
        str(final_model_dir)
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "TRAINING COMPLETE"
    )

    print(
        f"Model saved to:\n"
        f"{final_model_dir}"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":
    main()