from typing import List


def extract_lemmas(doc) -> List[str]:

    return [
        token.lemma_
        for token in doc
        if not token.is_space
    ]