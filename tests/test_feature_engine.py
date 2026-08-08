from humantrace.preprocessing.pipeline import preprocess
from humantrace.feature_engine.pipeline import extract_features


TEXT = """
Artificial intelligence is transforming education.
Students are increasingly using AI tools.
"""


def test_feature_extraction():

    document = preprocess(TEXT)

    features = extract_features(document)

    assert isinstance(features, dict)

    assert "word_count" in features
    assert "unique_word_count" in features
    assert "type_token_ratio" in features
    assert "lexical_density" in features

    print("\nFEATURES")

    for name, value in features.items():
        print(f"{name}: {value}")


if __name__ == "__main__":
    test_feature_extraction()