import requests
import json
import urllib.parse
from helper import load_csv, load_json


api_url = 'https://api.mobygames.com/v1'
api_key = urllib.parse.quote_plus('moby_uh7IolRAIDCHkSXaBYQatS1Y9ko')

def get_data(endpoint, params):
    params["api_key"]=  api_key
    response = requests.get(api_url+"/"+endpoint, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
    return response.json()

def get_games(genres=None, groups=None, platforms=None, format='brief'):
    endpoint = "/games"
    params = {
        "api_key": api_key,
        "genre" : genres,
        "group" : groups,
        "platform" : platforms,
        "format" : format
    }
    response= requests.get(api_url+endpoint, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
    return response.json()


def get_games_url(genres=None, groups=None, platforms=None,titles=None, format='id'):
    endpoint = "/games"
    params = {
        "api_key": api_key,
        "genre" : genres,
        "group" : groups,
        "platform" : platforms,
        "title" : titles,
        "format" : format
    }


    req = requests.Request('GET', api_url+endpoint, params=params)
    prepped = req.prepare()
    return prepped.url

def load_tags(tagtype):
        taglist=[]
        #load genres
        file_path = 'data/'+tagtype+'s.json'
        if tagtype == 'groups':
            data = load_csv(file_path)
        else:
            data =load_json(file_path)

        for genre in data[tagtype+'s']:
            taglist.append(
                {'tag' : genre[tagtype+'_name'], 
                 'id'  : genre[tagtype+'_id'],
                'type': tagtype
                }
            )
        return taglist

def get_moby_tags(keyword, taglist):

    tag_id = None
    tag_type = None
    for item in taglist:
        if item['tag'] == keyword:
           tag_id = item['id']
           tag_type = item['type']
           break
    return [tag_id,tag_type]








    