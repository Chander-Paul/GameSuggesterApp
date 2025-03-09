import keywordparser as kp
import mobyapi as moby
import similaritymodel as sim
import spacyparser as sp
import time


def generate_keywords(text):
    doc = sp.preprocess(text)
    keyword_chunks = sp.create_noun_chunks(doc)+sp.create_verb_chunks(doc)
    return keyword_chunks

#Generate Boolean Query using keywords and modifier chunks. Convert Keywords from user data to likely videogame tags
def generate_query(keyword_chunks, taglist, model):
    bool_query = sp.generate_query(keyword_chunks)
    
    for criteria in bool_query:
        criteria['gamekeyword'] = sim.get_most_similar_keywords(model, criteria['keyword'], [item['tag'] for  item in taglist])
        criteria['tag'] = moby.get_moby_tags(criteria['gamekeyword'], taglist)
    return bool_query

def generate_ranked_query(keyword_chunks, taglist, word_vectors):
    bool_query = sp.generate_query(keyword_chunks)
    keys = []
    
    
    for criteria in bool_query:

        ##Find the most similar keyword in the list of tags based on the their vector distance
        ##Only return cases with reasonable relevance of 0.4
        relevant_keywords=sim.most_similar_to_given_ranked(word_vectors, criteria['keyword'], [item['tag'] for  item in taglist], 1)
        for key in  relevant_keywords:
            if key[1]>=0.4:
                criteria['gamekeyword'] = key[0]
                criteria['tag'] = moby.get_moby_tags(criteria['gamekeyword'], taglist)
            else:
                bool_query.remove(criteria)
    return bool_query

def get_games(query):
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

    ##Change Platorms to an And nested Or to when multiple platforms are requested
    
    games = moby.get_games_url(params['genre'],params['group'], params['platform'], format='brief')
    games = moby.get_games(params['genre'],params['group'], params['platform'], format='brief')
    ##Sleep to not trigger timeout
    time.sleepp(3)
    not_games = moby.get_games(params['genre']+not_params['genre'],params['group']+not_params['group'], params['platform']+not_params['platform'], format='id')
    ##Filter games by negation list. 
    result = [game for game in games['games'] if game['game_id'] not in not_games]

    return games

def search_games(text):
    model = sim.load_model('models/fasttextsimilarity.model')
    taglist = moby.load_tags('genre')+moby.load_tags('group')+moby.load_tags('platform')
    keywords = generate_keywords(text)
    query = generate_ranked_query(keywords, taglist, model.wv)
    return get_games(query)