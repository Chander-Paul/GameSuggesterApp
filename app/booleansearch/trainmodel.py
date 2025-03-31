from helper import load_json, load_csv
import similaritymodel as sm
from gensim.models import FastText
import os
from config import config
import pathlib




path = str(pathlib.Path().resolve())+"/booleansearch/data/"
genres = load_json(str(path)+'genres.json')
platforms = load_json(path+'platforms.json')
groups = load_csv(path+'groups.csv')

##Add Genre/Group Decription through the sentence Some information is being lost in longer descriptions
sentences = [ genre["genre_name"]+"." + ".".join(
    
    [genre["genre_name"]+"."+description for description in genre["genre_description"].split(".") ]
    
    ) for genre in genres["genres"]]
del genres
sentences = [ group["group_name"]+"." + ".".join(
    
    [group["group_name"]+"."+description for description in group["group_description"].split(".") ]
    
    ) for group in groups]
del groups
sentences += [ platform["platform_name"] for platform in platforms["platforms"]]
del platforms

sentences = sm.preprocess(sentences)

model = FastText(sentences = sentences,sg=1, hs=0, 
                 vector_size=100, alpha=0.025, window=5, 
                 min_count=5, max_vocab_size=None, word_ngrams=1, 
                 sample=0.001, seed=1, workers=3, 
                 min_alpha=0.0001, negative=5, 
                 ns_exponent=0.75, cbow_mean=1,  
                 epochs=5, null_word=0, min_n=3, max_n=6, 
                 sorted_vocab=1, bucket=2000000, trim_rule=None, 
                 batch_words=10000, callbacks=(), max_final_vocab=None, shrink_windows=True)
# Save the model

model_path = str(pathlib.Path().resolve())+"/"+ config['model_path']+"/"+config['model_name']
model.save(model_path)
