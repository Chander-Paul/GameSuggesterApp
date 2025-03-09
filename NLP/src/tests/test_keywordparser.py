import unittest

import sys
import os
sys.path.insert(1, 'C:/Users/chand/OneDrive/Documents/Courses/repos/GameSuggesterApp/NLP/prototype')
from keywordparser import preprocess, parse_tree, extract_chunks

class TestKeywordParser(unittest.TestCase):

    def test_preprocess(self):
        text = "The quick brown fox jumps over the lazy dog."
        self.assertIsNotNone(preprocess(text))

    def test_parse_tree(self):
        tokens = preprocess("The quick brown fox jumps over the lazy dog.")
        tree = parse_tree(tokens)
        self.assertIsNotNone(tree)

    def test_extract_chunks(self):
        tokens = [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'), ('jumps', 'VB'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN')]
        tree = parse_tree(tokens)
        chunks = extract_chunks(tree)
        expected_chunks = {
            'NP': ['brown fox'],
            'VP': ['jumps over the lazy dog'],
            'AP':[]
        }

    def test_extract_chunks_adverb(self):
        tokens = [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'), ('did', 'VBZ'), ('not', 'RB'), ('jump', 'VB'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN')]
        tree = parse_tree(tokens)
        chunks = extract_chunks(tree)
        expected_chunks = {
            'NP': ['brown fox'],
            'VP': [],
            'AP':[['not', ' jump over the lazy dog']]
        }

        self.assertEqual(chunks, expected_chunks)
"""
        def test_extract_chunks_with_conjunctions(self):
            tokens = [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'), ('jumps', 'VB'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'), ('dog', 'NN'), ('and', 'CC'), ('the', 'DT'), ('cat', 'NN')]
            tree = parse_tree(tokens)
            chunks = extract_chunks(tree)
            expected_chunks = {
                'NP': ['brown fox', 'the cat'],
                'VP': ['jumps over the lazy dog'],
                'AP':[]
            }

            self.assertEqual(chunks, expected_chunks)
"""
if __name__ == '__main__':
    unittest.main()