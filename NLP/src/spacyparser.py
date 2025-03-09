from bs4 import BeautifulSoup
#from nltk.tree import ParentedTree

import spacy
from spacy.matcher import Matcher

def preprocess(text):
    text = BeautifulSoup(text, "lxml").text

    #add spacy processing piples
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("merge_entities")
    nlp.add_pipe("merge_noun_chunks")
    
    doc = nlp(text)
    return doc

def print_dependency_tree(doc):

    for token in doc:
        print(f"{token.text} -> {token.dep_} -> {token.head.text} pos {token.head.pos_}")

def get_conjunctions(doc):
    checked = 0
    conjunctions= []
    for tok in doc:
        if tok.i < checked: continue
        ##if tok.pos_ not in ('NOUN', 'PROPN'): continue
        if tok.conjuncts:
            conjunctions.append(tok, doc[tok.left_edge.i:tok.right_edge.i+1])
            checked = tok.right_edge.i + 1
    return conjunctions

##Takes a spacy doc object
def create_noun_chunks(doc):
    chunks = []
    conjunctions = []
    #filter on chunks from spacy noun chunks ignoring pronouns.
    for chunk  in doc.noun_chunks:
        if "PRON" not in  [t.pos_ for t in chunk] and chunk:
            neg_adverbs =[]
            conjunctions =[]
            
            ##For all tokens to the left of the token in dependency tree identify negative adverbs and store for later
            if chunk.root.dep_ :
                for w in chunk.root.head.lefts:
                    if w.dep_ == "neg":
                        neg_adverbs.append([doc[w.left_edge.i:w.right_edge.i+1]])

               ##For all the tokens to the right of the token identify conjunctions and store for later
                for w in chunk.root.head.rights:
                    if w.conjuncts:
                        conjunctions.append(doc[w.left_edge.i:w.right_edge.i+1])
            
            chunks.append([chunk.text.replace('games',''), neg_adverbs, conjunctions])
    return chunks

def create_verb_chunks(doc):
    chunks = []
    for chunk  in doc:
        if "VERB" ==  chunk.pos_:
            neg_adverbs =[]
            conjunctions =[]
            phrase =None
            for w in chunk.head.lefts: 
                if w.dep_ == "neg":
                    neg_adverbs.append(doc[w.left_edge.i:w.right_edge.i+1])
            for w in chunk.rights:
                if w.conjuncts:
                    conjunctions.append(doc[w.left_edge.i:w.right_edge.i+1])
                if w.dep_ in ('dobj','pobj'):
                    phrase = doc[w.left_edge.i:w.right_edge.i+1]
            chunks.append([chunk.text, neg_adverbs, conjunctions])
    return chunks


def  generate_query(chunks):
    query= []

    for chunk in chunks:
        query.append(
            {'keyword': chunk[0],
             'negation': chunk[1],
             'relation': chunk[2]
            }
        )
    return query


##Extract collective nouns and longer verb phrases
def console_matcher(doc):
    # Initialize the matcher with the shared vocab
    matcher = Matcher(doc.vocab)
    
    #Create grammer
    patterns = [
        {"label": "CN", "pattern": [{"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "NOUN"}]},
        {"label": "VP", "pattern": [{"POS": "VERB"}, {"POS": "NOUN", "OP": "?"}, {"POS": "ADP", "OP": "?"}, {"POS": "PART", "OP": "?"}, {"POS": "VERB", "OP": "?"}]},
        {"label": "AP", "pattern": [{"POS": "ADV"}, {"POS": "NOUN", "OP": "?"}, {"POS": "VERB", "OP": "?"}]}
    ]

    for pattern in patterns:
        matcher.add(pattern["label"], [pattern["pattern"]])
    
    # Apply the matcher to the doc
    matches = matcher(doc)
    

    chunks = []
    for match_id, start, end in matches:
        if doc.vocab.strings[match_id] in ('VP', 'CN'):
            span = doc[start:end]
            chunks.append((doc.vocab.strings[match_id], span))
    return chunks