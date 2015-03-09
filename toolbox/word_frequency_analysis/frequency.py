"""
    Analyzes the word frequencies in a book downloaded from
    Project Gutenberg
"""

import string

def get_word_list(file_name):
    """ Reads the specified project Gutenberg book.  Header comments,
	punctuation, and whitespace are stripped away.  The function
    	returns a list of the words used in the book as a list.
	All words are converted to lower case.
    """
    # Read the file specified
    f = open(file_name,'r')
    lines = f.readlines()
    
    # Remove header text from lines
    curr_line = 0
    while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
        curr_line += 1
    lines = lines[curr_line + 1:]

    # Remove footer text from lines
    curr_line = -1
    while lines[curr_line].find('END OF THIS PROJECT GUTENBERG EBOOK') == -1:
        curr_line -= 1
    lines = lines[: curr_line]

    # Strip lines into words
    words = []
    for i in range(len(lines)):
        # Remove punctuation
        next_line = lines[i].translate(string.maketrans("",""), string.punctuation)
        next_line = next_line.lower()
        words += next_line.split()
    
    return words

def get_top_n_words(word_list, n):
    """ Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
    """
    d = dict()
    for w in word_list:
        d[w] = d.get(w, 0) + 1
    ordered_by_frequency = sorted(d, key=d.get, reverse=True)
    return ordered_by_frequency[0:n]

words = get_word_list('sonnets.txt')
print get_top_n_words(words, 100)
