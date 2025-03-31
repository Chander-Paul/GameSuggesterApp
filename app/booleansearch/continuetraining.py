from helper import load_json, load_csv
import similaritymodel as sm
from gensim.models import FastText
import os
import pathlib
from config import config


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


# Save the model
model_path = str(pathlib.Path().resolve())+"/"+ config['model_path']+"/"+config['model_name']
model = FastText.load(model_path)
model.train(sentences, total_examples=len(sentences), epochs=model.epochs)
model.save(model_path)