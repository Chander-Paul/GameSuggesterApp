import sys
import gamesearch as gs
import pathlib
from config import config
import mobyapi as moby
import similaritymodel as sim
import time
import pathlib
from config import config




def main():

    args = sys.argv[1:] 
    text = args[0]
    path = pathlib.Path().resolve()
    ##Switch to loading and saving vectors
    model = sim.load_model(str(path)+"/"+config['model_path']+"/" +config['model_name'])
    taglist = gs.moby.load_tags('genre')+moby.load_tags('platform')##+moby.load_tags('group')
    #print(text)
    keywords = gs.generate_keywords(text)
    #print(keywords)
    results = gs.generate_ranked_query(keywords, taglist, model.wv)
    #print(results)
    #for i, keyword in enumerate(results):
    #            print(keyword['keyword']+", "+keyword['gamekeyword']+" "+str(keyword['score']))


# Using the special variable 
# __name__
if __name__ == "__main__":
    main()
