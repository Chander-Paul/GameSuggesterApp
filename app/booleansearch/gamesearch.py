import keywordparser as kp
import mobyapi as moby
import similaritymodel as sim
import spacyparser as sp
import time
import pathlib
from config import config





##Generate Keywords from User Input
def generate_keywords(text):
    doc = sp.preprocess(text)
    keyword_chunks = sp.create_noun_chunks(doc)+sp.create_verb_chunks(doc)
    return keyword_chunks

##Using Word Embeddings identify Keywords most similar to the User's Input
def generate_ranked_query(keyword_chunks, taglist, word_vectors):

    ##Assign Negations and Conjunctions to keys for better filtering##
    bool_query = sp.generate_query(keyword_chunks)
    results= []
    for criteria in bool_query:
        ##Find the most similar keyword in the list of tags based on the their vector distance 
        relevant_keywords=sim.most_similar_to_given_ranked(word_vectors, criteria['keyword'], [item['tag'] for  item in taglist], 1)
        for key in  relevant_keywords:
            if key[1]>=0.75:
                criteria['gamekeyword'] = key[0]
                criteria['tag'] = moby.get_moby_tags(criteria['gamekeyword'], taglist)
                criteria['score'] = key[1]
                results.append(criteria)
    return results


##Get Games from MOBYAPI Endpoint using Query##
def get_games(query, limit=10):
    ##Separate Boolean Filter Parameters into positive and negative filter parameters.
    params = {
        'genre' : [],
        'group' : [],
        'platform' : []
    }
    not_params = {
        'genre' : [],
        'group' : [],
        'platform' : []
    }
    for criteria in query:
        if criteria['negation']:
            continue
        if 'tag' in criteria:
            params[criteria['tag'][1]].append(criteria['tag'][0])

    print(f"URL \n{moby.get_games_url(params['genre'],params['group'], format='normal')}")
    
    ##Return games from MOBYAPI Endpoint
    ##Due to the exclusionary nature of most gaming platforms, platform filters are always treated as an OR
    if len(params['platform'])>1:
        games = moby.get_games(params['genre'],params['group'], format='normal',limit=limit)
        if games:
            filteredgames = games
            for game in filteredgames['games']:
                for platform in  game['platforms']:
                    if platform["platform_id"] not in params['platform']:
                        filteredgames['games'].remove(game)
                        break
                        ##games = [game for game in games['games'] if platform in [platform['platform_id'] for platform in game['platforms']]]
            ##In the case of no applicable platforms return the original unfiltered platform list
            if filteredgames['games']:
                games = filteredgames
    else:           
        games = moby.get_games(params['genre'],params['group'], params['platform'], format='normal',limit=limit)            

    ##Filter games by negation list. 
    results = []
    if games:
        for game in games['games']:
            for genre in game["genres"]:
                if genre["genre_id"] in not_params['genre']:
                    continue
            for platform in game["platforms"]:
                if platform["platform_id"] in not_params['platform']:
                    continue
            results.append(game)    

    return results

def search_games(text):
    path = pathlib.Path().resolve()
    model = sim.load_model(str(path)+"/"+config['model_path']+"/" +config['model_name'])
    taglist = moby.load_tags('genre')+moby.load_tags('platform')#+moby.load_tags('group')
    print(f"Potential MobyGames Filters \n {taglist[:3]} \n")
    keywords = generate_keywords(text)
    print(f"Extracted Keywords: \n{keywords} \n")
    query = generate_ranked_query(keywords, taglist, model.wv)
    print(f"Filtered Query \n{query} \n")
    return [get_games(query, limit=10),query]
















def generate_similar_keywords(keyword_chunks, taglist, word_vectors, n):
    bool_query = sp.generate_query(keyword_chunks)
    relevant_keys = []
    for criteria in bool_query:

        ##Find the most similar keyword in the list of tags based on the their vector distance

        relevant_keys.append(sim.most_similar_to_given_ranked(word_vectors, 
                                                           criteria['keyword'], 
                                                           [item['tag'].lower() for  item in taglist], n))


    return relevant_keys
