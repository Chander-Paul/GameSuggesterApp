from spacyparser import preprocess, create_noun_chunks, create_verb_chunks

text = "I like playing strategy and 4x games. I hate horror."
doc = preprocess(text)
print([chunk.conjuncts for chunk in doc.noun_chunks])