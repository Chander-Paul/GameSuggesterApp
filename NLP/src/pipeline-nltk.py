import re
import nltk
from nltk.tokenize import word_tokenize
#from nltk.chunk import RegexParser
from nltk import pos_tag
from gensim.models import FastText
from helper import load_json
from rake_nltk import Rake

#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger_eng')

text = "I want to play a game with base building, monster raising and crafting . PS5 player here. Howevever, I am not a fan of horror games"
text2 = 'What is a game where the setting feels like a "character" in its own right?' ##rake strips quotation marks that are used for emphasis

text = "I want to unload bullets into swarms of dudes- what do you suggest. Generally, don't want much more than that - hoards and hoards of dudes and a big ass gun. Don't need depth, don't need strategy, don't need to explore. Just want to unwind with massive waves of things to gun down."
words = word_tokenize(text)
pos_tags = pos_tag(words)

# Unicode Nomalization 
#tokenization based on boolean operators
#Identiy parts of speecg, Chunk based on divisors
#https://universaldependencies.org/u/pos/
##(VBP, IN, RB, RBR, RBS)sentiment  (", ", conjunction NNkeywords
#Issue tagging nouns as verb. May need to improve corpus 
#print("\nPoS Tagging Result:")
#print(pos_tags)

##chunking

grammar = """ preferences: {<VBP|IN|RB>+<NN|NNS>+(<CC|,>?<NN|NNS>+)+}"""
parser = nltk.RegexpParser(grammar)
tree = parser.parse(pos_tags)

##information extraction to get user boolean
#for s in tree.subtrees(lambda t: t.label() == "preferences"):
    #print(s)

#print(tree)


# Extraction given the list of strings where each string is a sentence.
#r.extract_keywords_from_sentences(<list of sentences>)

# To get keyword phrases ranked highest to lowest.
#print(r.get_ranked_phrases())

# To get keyword phrases ranked highest to lowest with scores.
#print(pos_tags)
##print((r.get_ranked_phrases_with_scores()))

##Keyword Extraction using Rake


r = Rake()

# Extraction given the text.
r.extract_keywords_from_text(text)



##Convert Keywords to APIKeys
model = FastText.load("models/fasttextsimilarity.model")
genres =  load_json('data/genres.json')
mobykeywords= []

for score, phrase, in r.get_ranked_phrases_with_scores():
        if score > 1: 
            mobykeywords.append([phrase, score, model.wv.most_similar_to_given(phrase, [item['genre_name'] for item in genres['genres']],)])

print(mobykeywords)
print(r.get_ranked_phrases_with_scores())


"""bool_query = ''
#for score, keyword in r.get_ranked_phrases_with_scores():
    if score > 1 :
        bool_query = bool_query + '"'+keyword+'"' + 'AND'
else:
    bool_query = bool_query[:-3]
print(bool_query)
"""





##regex to chunk sentence into the keywords and apply negation and dependency
#split into sentences. Treat each sentence as an AND unless there is 



