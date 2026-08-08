import numpy as np

from humantrace.feature_engine.base import FeatureExtractor
from humantrace.feature_engine.embeddings.model import (
    get_embedding_model
)


class EmbeddingFeatures(FeatureExtractor):

    name = "embeddings"

    def extract(self, document):

        sentences = document.sentences

        if len(sentences) < 2:
            return {
                "embedding_variance": 0.0,
                "embedding_similarity": 0.0,
            }

        model = get_embedding_model()

        embeddings = model.encode(
            sentences,
            convert_to_numpy=True
        )

        variance = float(
            np.mean(
                np.var(
                    embeddings,
                    axis=0
                )
            )
        )

        similarities = []

        for i in range(
            len(embeddings) - 1
        ):

            a = embeddings[i]
            b = embeddings[i + 1]

            denominator = (
                np.linalg.norm(a)
                * np.linalg.norm(b)
            )

            if denominator == 0:
                continue

            similarity = (
                np.dot(a, b)
                / denominator
            )

            similarities.append(
                float(similarity)
            )

        average_similarity = (
            sum(similarities)
            / len(similarities)
            if similarities
            else 0.0
        )

        return {

            "embedding_variance":
                variance,

            "embedding_similarity":
                average_similarity,
        }