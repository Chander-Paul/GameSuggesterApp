import unittest
from unittest.mock import patch

import sys
import os
sys.path.insert(1, 'C:/Users/chand/OneDrive/Documents/Courses/repos/GameSuggesterApp/NLP/prototype')

import mobyapi
import requests

class TestMobyAPI(unittest.TestCase):

    def test_get_games_url(self):
        expected_data = 'https://api.mobygames.com/v1/games?api_key=moby_uh7IolRAIDCHkSXaBYQatS1Y9ko&genre=1&genre=106&group=8656&platform=203&format=id'
        status_code = 200


        genres = ["1","106"] #RPG, 1st person
        groups = "8656" #RPG, 1st person
        platforms = "203"
        titles = None
        limit = 10
        format = 'id'
        result = mobyapi.get_games_url(genres, groups, platforms, titles, format)
        print(result)
        self.assertEqual(result, expected_data)
#https://api.mobygames.com/v1/games?format=normal&genre=106&genre=7&platform=203&limit=10&group=8656
    def test_get_games_success(self):
        expected_data = {"games": [137306, 137307]}
        status_code = 200


        genres = ["106","7"] #RPG, 1st person
        groups = "8656" #RPG, 1st person
        platforms = "203"
        titles = None
        limit = 10
        format = 'id'
        result = mobyapi.get_games(genres, groups, platforms, titles, format)

        self.assertEqual(result, expected_data)

        


    

     

if __name__ == '__main__':
    unittest.main()