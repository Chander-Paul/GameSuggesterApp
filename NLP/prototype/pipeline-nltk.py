import re
import nltk
from nltk.tokenize import word_tokenize
#from nltk.chunk import RegexParser
from nltk import pos_tag

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

text = "I want to play a game with base-building, monster raising and crafting elements. PS5 player here"

words = word_tokenize(text)
pos_tags = pos_tag(words)

# Unicode Nomalization 
#tokenization based on boolean operators
#Identiy parts of speecg, Chunk based on divisors
#https://universaldependencies.org/u/pos/

#Issue tagging nouns as verb. May need to improve corpus 
print("\nPoS Tagging Result:")
for word, pos_tag in pos_tags:
    print(f"{word}: {pos_tag}")
  
