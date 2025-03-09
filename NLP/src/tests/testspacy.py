import spacy
from spacy.matcher import Matcher, DependencyMatcher
sentence = "I want to unload bullets into swarms of dudes- what do you suggest. Generally, do not want much more than that, hordes of dudes and a big ass gun. Don't need depth. don't need strategy. don't need to explore. Just want to unwind with massive waves of things to gun down."


nlp = spacy.load("en_core_web_sm")
doc = nlp(sentence)
"""
for token in doc:
    if token.conjuncts:
        conjuncts = token.conjuncts             # tuple of conjuncts
        print("Conjuncts for ", token.text)
        relation = doc[conjuncts[0].i]
        print(relation.left_edge)
        print(doc[relation.left_edge.i:relation.i+1])
"""
matcher = DependencyMatcher(nlp.vocab)
pattern = [
    {
        "RIGHT_ID": "noun",
        "RIGHT_ATTRS": {"POS": "NOUN"}
    },
    {
        "LEFT_ID": "noun",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": "prep"}
    },
    {
        "LEFT_ID": "prep",
        "REL_OP": ">",
        "RIGHT_ID": "noun2",
        "RIGHT_ATTRS": {"DEP": "pobj"}
    }
]
matcher.add("PROPOSITIONAL_VERB", [pattern])
matches = matcher(doc)

for match in matches:
    verb = doc[match[1][0]]
    prop = doc[match[1][1]]
    noun2 = doc[match[1][2]]
    print(f'{verb} - {prop}-{noun2}')