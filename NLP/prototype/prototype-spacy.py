import spacy
nlp = spacy.load("en_core_web_sm")


text = "I want to play a game with base building, monster raising and crafting elements. PS5 player here"
text2 = "I want to play a game like dark souls with some Roguelike mechanics"
doc = nlp(text2)

# Unicode Nomalization 
#tokenization based on boolean operators
#Identiy parts of speecg, Chunk based on divisors
#https://universaldependencies.org/u/pos/
 
#words like mechanics, elements maybe mislabeled as part of a whole word
print("\nPoS Tagging Result:")
for token in doc:
    print(f"{token.text}: {token.pos_}")
  
