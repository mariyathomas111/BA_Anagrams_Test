import unittest
import tempfile
import os
from anagrams import Anagrams

class TestAnagrams(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary file with a controlled word list
        cls.test_words = [
            "plates", "palest", "pastel", "petals", "staple",
             "tea", "ate","eat",
            "dog", "god",
            "abbey","tan","ant"
        ]
        cls.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        for word in cls.test_words:
            cls.temp_file.write(word + "\n")
        cls.temp_file.close()
        # Reset the singleton dictionary for isolated tests
        Anagrams._anagram_dict = None

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.temp_file.name)

    def setUp(self):
        # Reset the dictionary before each test to ensure isolation
        Anagrams._anagram_dict = None

    def test_get_anagrams_basic(self):
        anagrams = Anagrams(self.temp_file.name)
        self.assertEqual(anagrams.get_anagrams('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])
        self.assertEqual(anagrams.get_anagrams('eat'), ['ate', 'eat', 'tea'])
        self.assertEqual(anagrams.get_anagrams('dog'), ['dog', 'god'])

    def test_get_anagrams_missing(self):
        anagrams = Anagrams(self.temp_file.name)
        self.assertEqual(anagrams.get_anagrams('missingword'), [])
        self.assertEqual(anagrams.get_anagrams(''), [])

    def test_get_anagrams_case_sensitive(self):
        anagrams = Anagrams(self.temp_file.name)
        # 'Eat' (capital E) will return nothing if words are all lowercase
        self.assertEqual(anagrams.get_anagrams('Eat'), [])

    def test_non_string_input(self):
        anagrams = Anagrams(self.temp_file.name)
        with self.assertRaises(ValueError):
            anagrams.get_anagrams(123)
        with self.assertRaises(ValueError):
            anagrams.get_anagrams(None)
        with self.assertRaises(ValueError):
            anagrams.get_anagrams(['eat'])

    def test_file_not_found(self):
        with self.assertRaises(RuntimeError):
            Anagrams('does_not_exist.txt')

    def test_file_io_error(self):
        # Simulate by opening the file in exclusive mode (on Windows) or using a directory path on any OS
        with self.assertRaises(RuntimeError):
            Anagrams(os.path.dirname(self.temp_file.name))

    def test_thread_safety_and_singleton(self):
        # The second instance should not reload the dictionary
        anagrams1 = Anagrams(self.temp_file.name)
        # deliberately change the class dict to test singleton nature
        Anagrams._anagram_dict['xyz'] = ['test']
        anagrams2 = Anagrams(self.temp_file.name)
        self.assertIn('xyz', anagrams2.anagram_dict)

    def test_anagrams_for_single_word(self):
        anagrams = Anagrams(self.temp_file.name)
        # abbey in word list has no anagrams
        self.assertEqual(anagrams.get_anagrams('abbey'), ['abbey'])

    def test_anagrams_for_word_not_in_file_but_anagrams(self):
        anagrams = Anagrams(self.temp_file.name)
        # the entered word itself not in the file but its anagrams exist in the file
        self.assertEqual(anagrams.get_anagrams('nat'), ['ant','tan'])

if __name__ == '__main__':
    unittest.main()