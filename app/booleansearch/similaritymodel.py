
import nltk
from gensim.models import FastText, KeyedVectors
from gensim.parsing.preprocessing import remove_stopwords, preprocess_string
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer as wnl
from numpy import argsort, argmax, flip
from helper import load_json

def preprocess(data):
    words = []
    for doc in data:
        doc = BeautifulSoup(doc, "lxml").text
        sentences = nltk.sent_tokenize(doc)
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            tokens = [word.lower() for word in tokens]
            words.append(tokens)
    return words





def create_model(data, file_name, parameters):
    model = FastText(sentences=data, vector_size=100, window=5, min_count=1, workers=4)
    model.save(file_name)

    return model

def load_model(file_name):
    model = FastText.load(file_name)
    return model

def update_model(file_path, model_path, data, parameters):
    docs = data
    words = preprocess(docs)
    model = FastText.train(model_path, sentences = docs, params=parameters)
    return model

def load_vectors(file_path):
    vector_path= file_path #"models/fasttextsimilarity.model"
    return KeyedVectors.load(vector_path, mmap='r')

def save_vectors(model, file_path):
    word_vectors = model.wv
    word_vectors.save(file_path)

    
def get_most_similar_keywords(model, keyword, data):
    keyword = model.wv.most_similar_to_given(keyword, [item for item in data])
    return keyword



#See alternative words.
def most_similar_to_given_ranked(word_vectors, key1, keys_list, n):
    #Get the `key` from `keys_list` most similar to `key1`

    relevant_keys = []
    relevant_kays_list = []
    for key in keys_list:
        relevant_keys.append(word_vectors.similarity(key1, key))
    indices = flip(argsort(relevant_keys))
    i=0
    for index in indices:
        if i >= n:
            return relevant_kays_list
        relevant_kays_list.append([keys_list[index], relevant_keys[index]])
        i = i+1
    return relevant_kays_list
        
        
    

#print(most_similar_to_given_ranked(model.wv, 'stellaris', [item['genre_name'] for item in data['genres']],5 ))
#print(model.wv.most_similar_to_given('stellaris', [item['genre_name'] for item in data['genres']],))


##Add Groups to use as tags.
