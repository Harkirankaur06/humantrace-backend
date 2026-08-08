from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


MODEL_NAME = "distilgpt2"


_tokenizer = None
_model = None


def get_language_model():

    global _tokenizer
    global _model

    if _tokenizer is None:

        _tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME
        )

        _model.eval()

    return _tokenizer, _model