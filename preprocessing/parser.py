from typing import List, Dict


def extract_pos_tags(doc) -> List[str]:

    return [
        token.pos_
        for token in doc
        if not token.is_space
    ]



def extract_dependencies(doc) -> List[str]:

    return [
        token.dep_
        for token in doc
        if not token.is_space
    ]



def extract_linguistic_features(doc):

    return {

        "pos_tags":
        extract_pos_tags(doc),

        "dependencies":
        extract_dependencies(doc)

    }