import threading
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Anagrams:
    """
    A thread-safe, singleton-style class to quickly find all anagrams of a given word
    using a word list file. The anagram dictionary is loaded only once, even if multiple
    Anagrams instances are created.
    """
    _instance_lock = threading.Lock()
    _anagram_dict = None

    def __init__(self, word_file='words.txt'):
        """
        Initializes the Anagrams instance. If the anagram dictionary hasn't been loaded yet,
        it loads it from the given word file in a thread-safe manner.

        Args:
            word_file (str): Path to the word list file, one word per line.
        """
        if Anagrams._anagram_dict is None:
            with Anagrams._instance_lock:
                if Anagrams._anagram_dict is None:
                    anagram_dict = defaultdict(list)
                    try:
                        with open(word_file) as f:
                            for line in f:
                                word = line.strip()
                                if word:
                                    key = ''.join(sorted(word))
                                    anagram_dict[key].append(word)
                        logging.info(f"Successfully loaded words from '{word_file}'.")
                    except FileNotFoundError:
                        logging.error(f"Word file '{word_file}' not found.")
                        raise RuntimeError(f"Word file '{word_file}' not found.")
                    except IOError as e:
                        logging.error(f"Error reading file '{word_file}': {e}")
                        raise RuntimeError(f"Error reading file '{word_file}': {e}")
                    # Convert defaultdict to dict for thread safety and memory efficiency
                    Anagrams._anagram_dict = dict(anagram_dict)
        self.anagram_dict = Anagrams._anagram_dict
        #print( self.anagram_dict)

    def get_anagrams(self, word):
        """
        Returns a sorted list of all anagrams for the given word.

        Args:
            word (str): The word to find anagrams for.

        Returns:
            list: A sorted list of anagrams for the input word.
        """
        if not isinstance(word, str):
            logging.warning("Input word is not a string.")
            raise ValueError("Input word must be a string.")
        if not word:
            logging.info("Empty input word provided; returning empty list.")
            return []
        key = ''.join(sorted(word))
        result = sorted(self.anagram_dict.get(key, []))
        if result:
            logging.info(f"Found {len(result)} anagrams for '{word}'.")
        else:
            logging.info(f"No anagrams found for '{word}'.")
        return result

    

# Example usage:
if __name__ == "__main__":
    anagrams = Anagrams()
    logging.info("Anagram dictionary loaded successfully.")
    # print(anagrams.anagram_dict)
    test_words = ['eat', 'plates', 'abbey', 'testxyz', 'ant','nation']
    for w in test_words:
        anagrams_list = anagrams.get_anagrams(w)
        print(f"Anagrams for '{w}': {anagrams_list}")



