from bs4 import BeautifulSoup
import re
import spacy
from helper import load_text
from spacy.matcher import Matcher
import pathlib
from config import config



def preprocess(text):
    text = BeautifulSoup(text, "lxml").text

    #add spacy processing piples
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("merge_entities")
    nlp.add_pipe("merge_noun_chunks")
    text = re.sub(r'[^A-Za-z0-9 ,.\']+', ' ', text)
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
        if "PRON" not in  [t.pos_ for t in chunk] and   chunk and chunk.text.lower():
            neg_adverbs =[]
            conjunctions =[]
            extentions =[]

            ##For all tokens to the left of the token in dependency tree identify negative adverbs and store for later
            if chunk.root.dep_ :
                for w in chunk.root.head.head.head.lefts:
                    if w.dep_ == "neg":
                        neg_adverbs.append([doc[w.left_edge.i:w.right_edge.i+1]])

               ##For all the tokens to the right of the token identify conjunctions and store for later
                for w in chunk.root.head.rights:

                    extentions.append(doc[w.left_edge.i:w.right_edge.i+1])                  
                    if w.dep_ == "neg":
                        neg_adverbs.append([doc[w.left_edge.i:w.right_edge.i+1]])

                    if w.conjuncts:
                        conjunctions.append(doc[w.left_edge.i:w.right_edge.i+1])
            chunks.append([chunk.text, neg_adverbs, conjunctions,extentions])

    return chunks

def create_verb_chunks(doc):
    chunks = []
    for chunk  in doc:
        if "VERB" ==  chunk.pos_:
            neg_adverbs =[]
            conjunctions =[]
            phrase =None
            extentions = []
            if chunk.dep_ :
                for w in chunk.head.lefts:
                    if w.dep_ == "neg":
                        neg_adverbs.append([doc[w.left_edge.i:w.right_edge.i+1]])

               ##For all the tokens to the right of the token identify conjunctions and store for later
                for w in chunk.head.rights:
                    extentions.append(doc[w.left_edge.i:w.right_edge.i+1])
                    if w.dep_ == "neg":

                        neg_adverbs.append([doc[w.left_edge.i:w.right_edge.i+1]])
   


                    if w.conjuncts:
                        conjunctions.append(doc[w.left_edge.i:w.right_edge.i+1])
            
            
                    phrase = doc[w.left_edge.i:w.right_edge.i+1]
            chunks.append([chunk.text, neg_adverbs, conjunctions, extentions])
    return chunks


def  generate_query(chunks):
    query= []
    path = str( pathlib.Path().resolve())
    stop_words = load_text(path+"/"+ config['data_path']+"/"+'english.txt')

    ##Remove stopwords and overrepresented words such as "Games" "Play"
    negatives= []

    for chunk in chunks:
        negatives.append([token.text.replace(chunk[0],'') for token in chunk[3] if chunk [1] ])
    for chunk in chunks:
        tokens = chunk[0].split()
        tokens = [token for token in tokens if token.lower() not in stop_words]
        chunk[0] = ' '.join(str(token) for token in tokens)

        if chunk[0].replace(' ','') !='':
            for token in negatives:
                for word in token:
                    if chunk[0] in word:
                        chunk[1] = 'not'
                        break
            query.append(
                {'keyword': chunk[0].lower(),
                'negation': chunk[1],
                'relation': chunk[2]
                }
            )
    return query

