from humantrace.preprocessing.pipeline import preprocess



text = """
Artificial intelligence is transforming education.

Students are increasingly using AI tools.
"""


document = preprocess(text)


print("\nTEXT")
print(document.clean_text)


print("\nPARAGRAPHS")
print(document.paragraphs)


print("\nSENTENCES")
for s in document.sentences:
    print("-", s)


print("\nTOKENS")
print(document.tokens)


print("\nLEMMAS")
print(document.lemmas)


print("\nPOS TAGS")
print(document.pos_tags)


print("\nDEPENDENCIES")
print(document.dependencies)