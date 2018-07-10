"""Generate Markov text from text files."""

from random import choice
import sys

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # your code goes here

    with open(file_path, 'r') as f:
    	file_text = f.read()

    return file_text


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    # your code goes here

    word_list = text_string.split()

    for i, word in enumerate(word_list):

    	# current key tuple
    	temp_key = (word, word_list[i+1])

    	# prevent out of range indexing
    	if i == len(word_list)-2:
    		chains[temp_key] = None
    		break

    	# add next value to dictionary
    	if temp_key in chains:
    		# already in dict, only add follwing word
    		chains[temp_key].append(word_list[i+2])
    	else:
    		# not in dict, add both key and following word
    		chains[temp_key] = [word_list[i+2]]

    return chains


def make_text(chains):
    """Return text from chains."""

    # Init words list
    words = []

    # Start words list
    start_point = choice(list(chains.keys()))
    words.extend(start_point)
    key = start_point
    
    while True:
    	# add words to list
    	if chains[key] == None:
    		# at end of text
    		break
    	else:
    		# choose new link
    		link = choice(chains[key])

    		# add new link to words
    		words.append(link)

    		# create next key
    		key = (key[1],link)

    return " ".join(words)


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)
print(random_text)
