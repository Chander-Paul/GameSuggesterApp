from nltk import word_tokenize, pos_tag, RegexpParser, sent_tokenize
from nltk.tree import ParentedTree
from nltk.stem import WordNetLemmatizer



def preprocess(text):
    wnl = WordNetLemmatizer()
    sentences = sent_tokenize(text)
    tokens = [wnl.lemmatize(word) for sent in sentences for word in word_tokenize(sent)]

    # Get the part of speech tags
    return pos_tag(tokens)


def parse_tree(tokens):
    # Grammar for extracting Noun Phrases, Verb Phrases for keywords and Adverbs for Sentiment.
    grammar = r"""
                    CN: {<N.*><IN><N.*>}            #Collective Nouns
                    NP: {<DT>?<JJ>?<N.*|CN>}        #Noun phrases
                    TOV: {<TO><V.*>}                #Group verb phrases beginning with to
                    PP: {<IN><NP>}                  #Prepositional Phrases
                    VP: {<V.*><NP|PP|TOV>}          #Verb Phrases
                    AP: {<RB><NP|VP>}               #Adverb Phrases
    """
    # Chunk texts based on grammar
    chunk_parser = RegexpParser(grammar)
    return chunk_parser.parse(tokens)

def extract_chunks(tree):
    chunks = {
        'NP': [],
        'VP': [],
        'AP': []
    }
    ptree = ParentedTree.convert(tree) #Add Parentedtree to parent nodes. Trees should be ignored if part of a higher order tree
    pos = 0
    for subtree in ptree.subtrees():
        if subtree.label() == 'NP' and subtree.parent().label() == 'S':
            chunks['NP'].append( [pos,' '.join(word for word, tag in subtree.leaves())])
        elif subtree.label() == 'NP' and subtree.parent().label() == 'PP':
            if subtree.parent().parent().label() == 'S':
                chunks['NP'].append([pos, ' '.join(word for word, tag in subtree.leaves())])
        elif subtree.label() == 'VP' and subtree.parent().label() != 'AP':
            chunks['VP'].append([pos, ' '.join(word for word, tag in subtree.leaves())])
        elif subtree.label() == 'AP':
            adverb = ''
            keyphrase = ''
            for word, tag in subtree.leaves():
                if tag == 'RB':
                    adverb = word  # Append adverb as its own cell
                else:
                    keyphrase += ' ' + word  # Join the words to keyphrase
            chunks['AP'].append([pos, adverb, keyphrase])
        pos += 1
    return chunks




##Note add conjunctions to the list of chuncks. Add Depdency for conjunctions and sentences.

def is_negation_adverb(word):
    negation_adverbs = ["n't", "not", "never", "no", "neither", "nor", "nowhere", "hardly", "scarcely", "barely"]
    return word.lower() in negation_adverbs

def convert_to_bool_query(chunks):



    query = {
        'NP': [],
        'VP': [],
        'AP': []
    }
    for chunk in chunks['NP']:
        query['NP'].append(chunk)
    for chunk in chunks['VP']:
        query['VP'].append(chunk)
    for chunk in chunks['AP']:
            if is_negation_adverb(chunk[1]):
                query['NP'].append([chunk[0], "NOT", chunk[2]])
            else:
                query['NP'].append([chunk[0],"YES", chunk[2]])
    return query
#text = "I want to unload bullets into swarms of dudes- what do you suggest. Generally, do not want much more than that - hoards and hoards of dudes and a big ass gun. Don't need depth, don't need strategy, don't need to explore. Just want to unwind with massive waves of things to gun down."
#print(convert_to_bool_query(extract_chunks(parse_tree(preprocess(text)))))
#print(extract_chunks(parse_tree(preprocess(text))))
def generate_query(text):
    return convert_to_bool_query(extract_chunks(parse_tree(preprocess(text))))