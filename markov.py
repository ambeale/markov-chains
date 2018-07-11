"""Generate Markov text from text files."""

from random import choice
import sys

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path, 'r') as f:
        file_text = f.read()

    # if corpus does not end in punctuation, append new random punctuation
    if file_text[-1] not in ["?",".","!"]:
        file_text = file_text.rstrip()
        file_text += choice(["?",".","!"])

    return file_text


def make_chains(text_string, n):
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

    word_list = text_string.split()

    for i, word in enumerate(word_list):
        # init list that will become key tuple
        create_tuple = []

        # grabbing n words for n-gram
        for j in range(i,i+n):
            create_tuple.append(word_list[j])

        # current key tuple
        temp_key = tuple(create_tuple)

        # prevent out of range indexing
        if i == len(word_list)-n:
            chains[temp_key] = None
            break

        # add next value to dictionary
        if temp_key in chains:
            # already in dict, only add follwing word
            chains[temp_key].append(word_list[i+n])
        else:
            # not in dict, add both key and following word
            chains[temp_key] = [word_list[i+n]]

    return chains


def get_new_key(link, old_key):
    """Create next key; return tuple of new key"""

    temp_key_list = []

    # build list with last n words
    for i, word in enumerate(old_key):
        if i > 0:
            temp_key_list.append(word)

    # create new key
    temp_key_list.append(link)
    return tuple(temp_key_list)

def make_text(chains, n):
    """Return text from chains."""

    # Init words list
    words = []

    # Start words list
    start_point = choice(list(chains.keys()))
    while not start_point[0][0].isupper():
        start_point = choice(list(chains.keys()))

    words.extend(start_point)
    key = start_point
    
    # add words to list
    while True:
        if chains[key] == None:
            # end of Markov chain
            break
        
        # set max number of characters
        elif len(" ".join(words)) > 500:
            # choose new link
            link = choice(chains[key])

            # add new link to word if ends in punctuation; else pick new key
            if link[-1] in ["?",".","!"]:
                words.append(link)
                break
            else:
                # choose a new key
                key = get_new_key(link, key)

        else:
            # choose new link
            link = choice(chains[key])

            # add new link to words
            words.append(link)

            # choose a new key
            key = get_new_key(link, key)

    return " ".join(words)


# assign variables to standard inputs (n value and at least one input file required)
n = int(sys.argv[1])
input1 = sys.argv[2]

# If two files, open both and combine the strings. Else, open one file.
try:
    input2 = sys.argv[3]
    input_text = open_and_read_file(input1) + open_and_read_file(input2)
except:
    input_text = open_and_read_file(input1)

# Get a Markov chain
chains = make_chains(input_text, n)

# Produce random text
random_text = make_text(chains, n)
print(random_text)
