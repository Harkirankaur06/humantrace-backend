from humantrace.config.nlp import nlp

from humantrace.preprocessing.cleaner import (
    clean_text
)

from humantrace.preprocessing.tokenizer import (
    extract_paragraphs,
    extract_sentences,
    extract_tokens
)

from humantrace.preprocessing.lemmatizer import (
    extract_lemmas
)

from humantrace.preprocessing.parser import (
    extract_pos_tags,
    extract_dependencies
)

from humantrace.core.document import EssayDocument



def preprocess(
    text: str
) -> EssayDocument:
    """
    Complete preprocessing pipeline.
    """

    cleaned = clean_text(text)


    doc = nlp(cleaned)


    return EssayDocument(

        raw_text=text,

        clean_text=cleaned,

        paragraphs=
        extract_paragraphs(cleaned),

        sentences=
        extract_sentences(doc),

        tokens=
        extract_tokens(doc),

        lemmas=
        extract_lemmas(doc),

        pos_tags=
        extract_pos_tags(doc),

        dependencies=
        extract_dependencies(doc)

    )