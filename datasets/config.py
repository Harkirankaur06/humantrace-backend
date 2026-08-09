from pathlib import Path

# ROOT DIRECTORIES

DATASET_DIR = Path(__file__).resolve().parent

RAW_DIR = DATASET_DIR / "raw"

PROCESSED_DIR = DATASET_DIR / "processed"

SPLITS_DIR = DATASET_DIR / "splits"

METADATA_DIR = DATASET_DIR / "metadata"


# RAW DATA DIRECTORIES

RAW_HUMAN_DIR = RAW_DIR / "human"

RAW_AI_DIR = RAW_DIR / "ai"

RAW_AI_POLISHED_DIR = RAW_DIR / "ai_polished"

RAW_HUMAN_REVISED_DIR = RAW_DIR / "human_revised"


# OUTPUT FILES

MERGED_DATASET = PROCESSED_DIR / "merged_dataset.jsonl"

TRAIN_DATASET = SPLITS_DIR / "train.jsonl"

VALIDATION_DATASET = SPLITS_DIR / "validation.jsonl"

TEST_DATASET = SPLITS_DIR / "test.jsonl"


# RANDOMNESS

RANDOM_SEED = 42


# DATASET SETTINGS

TRAIN_SPLIT = 0.80

VALIDATION_SPLIT = 0.10

TEST_SPLIT = 0.10


# FILTERS

MIN_WORDS = 100

MAX_WORDS = 1200

LANGUAGE = "en"


# LABELS

VALID_LABELS = {

    "human",

    "ai",

    "ai_polished",

    "human_revised"

}