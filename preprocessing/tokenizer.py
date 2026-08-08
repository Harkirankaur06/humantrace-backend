from typing import List


def extract_paragraphs(
    text: str
) -> List[str]:

    paragraphs = [
        p.strip()
        for p in text.split("\n")
        if p.strip()
    ]

    return paragraphs



def extract_sentences(doc) -> List[str]:

    return [
        sent.text.strip()
        for sent in doc.sents
    ]



def extract_tokens(doc) -> List[str]:

    return [
        token.text
        for token in doc
        if not token.is_space
    ]