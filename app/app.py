from flask import Flask, render_template, request
from flask.views import View


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
        results = search_games(input)
        games = results[0]
        filters = results[1]

        if not games:
            return render_template('index.html', input = input, filters = filters)
        return render_template('results.html', games = games, input = input, filters = filters)
    return render_template('index.html')


