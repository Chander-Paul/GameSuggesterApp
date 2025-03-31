# Game Suggester

The Game Suggester is a web app that reccomends a user a video game based on their a description of their game
preferences. It utilizes concepts such as dependency parsing and word embeddings to extract information from 
a user's input then searches for an appropriate game on the MobyGames database. 

## Installation

We suggest creating a virtual environment such as venv

```bash
pip install -r requirements.txt

```
## Downloadding Data

This application relies on additional external datasets which maybe unavaiable on the user's device,
These can be downloaded through the command

```bash
python booleansearch/config-download.py
```
##Loading the app
This program runs as a Flask web app. To start the application simply run the following command in the "app"
folder

```bash
python -m flask  run
```

## Usage

To access the application open your web browser and connect to the link provided by Flask. The default location is

http://127.0.0.1:5000





Additional Code Refences

Larger stopwords list
Additional stop-words: https://github.com/Alir3z4/stop-words/blob/master/english.txt
0