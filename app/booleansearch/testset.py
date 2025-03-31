import sys
import gamesearch as gs
import pathlib
from config import config
import mobyapi as moby
import similaritymodel as sim
import time
import pathlib
from config import config
from helper import load_csv, save_json_to_csv
from difflib import SequenceMatcher




def main():


    path = pathlib.Path().resolve()
    ##Switch to loading and saving vectors
    model = sim.load_model(str(path)+"/"+config['model_path']+"/" +config['model_name'])
    taglist = gs.moby.load_tags('genre')+moby.load_tags('platform')##+moby.load_tags('group')
    data = load_csv('booleansearch/data/testphase4(in).csv')
    for input in data:
        keywords = gs.generate_keywords(input['userinput'])
        results = gs.generate_ranked_query(keywords, taglist, model.wv)
        relevant_keywords = []
        for i, keyword in enumerate(results):
                if i == len(results) - 1:

                    relevant_keywords.append(keyword['gamekeyword'])
                    break
                else:
                    relevant_keywords.append(keyword['gamekeyword']+",")
        input['ExtratedKeys'] = relevant_keywords
        score_agg = 0
        for expected_key in input['ExpectedKeywords'].split(","):
            max = 0
            for x in  input['ExtratedKeys']:
                score = SequenceMatcher(None, expected_key, x).ratio()
                if max < score:
                     max = score
            score_agg = score_agg+max
        input['Positive'] = score_agg/len(input['ExpectedKeywords'].split(","))
             
    save_json_to_csv(data, 'booleansearch/data/testphase6.csv')




# Using the special variable 
# __name__
if __name__ == "__main__":
    main()
