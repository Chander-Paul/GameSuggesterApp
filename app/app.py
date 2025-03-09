###Remember to add to github DONT FORGET
##ADD A GITHUB NOW
from flask import Flask, render_template, request##, jsonify
from flask.views import View
#from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/booleansearch')))
from booleansearch.gamesearch import search_games


app  = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/submit", methods = ['GET','POST'])
def results():
    if request.method =='POST':
        input = request.form['game_input']
        ##games = search_games(input)
        games ={
                "games": [
                    {
                    "game_id": 23,
                    "moby_url": "https://www.mobygames.com/game/23/the-ancient-art-of-war/",
                    "title": "The Ancient Art of War"
                    },
                    {
                    "game_id": 156,
                    "moby_url": "https://www.mobygames.com/game/156/dungeon-keeper/",
                    "title": "Dungeon Keeper"
                    }
                ]
        }
        return render_template('results.html', games = games["games"])
    return render_template('index.html')


