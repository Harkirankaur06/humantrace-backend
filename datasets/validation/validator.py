REQUIRED_FIELDS = {
    "essay_id",
    "text",
    "label",
    "source",
}


VALID_LABELS = {
    "human",
    "ai",
    "ai_polished",
    "human_revised",
}


def validate_record(record: dict) -> None:

    missing = REQUIRED_FIELDS - record.keys()

    if missing:
        raise ValueError(
            f"Missing required fields: {sorted(missing)}"
        )

    if not isinstance(record["text"], str):
        raise TypeError(
            "Essay text must be a string"
        )

    if not record["text"].strip():
        raise ValueError(
            "Essay text cannot be empty"
        )

    if record["label"] not in VALID_LABELS:
        raise ValueError(
            f"Invalid label: {record['label']}"
        )