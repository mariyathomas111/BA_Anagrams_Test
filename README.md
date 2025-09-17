Anagram-problem statement:

# Given a words.txt file containing a newline-delimited list of dictionary
# words, please implement the Anagrams class so that the get_anagrams() method
# returns all anagrams from words.txt for a given word.
#
# Bonus requirements:
#   - Optimise the code for fast retrieval
#   - Write more tests
#   - Thread safe implementation

import unittest

class Anagrams:

    def __init__(self):
        self.words = open('words.txt').readlines()

    def get_anagrams(self, word):
        pass


class TestAnagrams(unittest.TestCase):

    def test_anagrams(self):
        anagrams = Anagrams()
        self.assertEquals(anagrams.get_anagrams('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])
        self.assertEquals(anagrams.get_anagrams('eat'), ['ate', 'eat', 'tea'])


if __name__ == '__main__':
    unittest.main()




Summary of the fix:

anagrams.py contains the code
test_anagrams.py contains the unit tests
words.txt file containing the words

Overview of the code:
The dictionary always contains every word, even singletons.
get_anagrams returns ['word'] if the word is in the file but has no other anagrams.

If the word and it's anagrams not in the file, it returns [].

if the word itself is not in the file but its anagrams exists in the fille, it returns the existing anagrams from the file
for ex: we have the words  'ant','tan'  in words.txt but no 'nat'. so if we try 
anagrams.get_anagrams('nat') = ['ant', 'tan']


overview of the design : 

Singleton-Style Load: The dictionary is loaded only once, no matter how many times the class is instantiated.
Thread Safety: The double-check pattern with a lock ensures multiple threads don’t try to load the file at the same time.
Building the Anagram Dictionary:
For each word in the file, sorts the letters to create a key.
Example: 'eat', 'tea', and 'ate' all have the key 'aet'.
Stores all words with the same key together.
Persistent Storage: Once loaded, all Anagrams instances use the same dictionary.

Efficiency: Anagrams lookup is O(1) per word, since dictionary keys are precomputed.




