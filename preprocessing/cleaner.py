import re
import unicodedata


def normalize_unicode(text: str) -> str:
    """
    Normalize unicode characters.
    Converts different representations
    of the same character.
    """

    return unicodedata.normalize(
        "NFKC",
        text
    )


def remove_extra_spaces(text: str) -> str:
    """
    Remove unnecessary whitespace.
    """

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()



def clean_text(text: str) -> str:
    """
    Complete cleaning pipeline.
    """

    text = normalize_unicode(text)

    text = remove_extra_spaces(text)

    return text