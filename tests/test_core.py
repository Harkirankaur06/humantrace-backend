from humantrace.core.document import EssayDocument


doc = EssayDocument(
    raw_text="HumanTrace is amazing."
)


print(doc.word_count)


doc.tokens = [
    "HumanTrace",
    "is",
    "amazing"
]


print(doc.word_count)