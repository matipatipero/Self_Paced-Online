#!/usr/bin/env python3

# Matias Li-Pino
# UW python lesson 4 - trigrams
# Trigram analysis is very simple. Look at each set of three adjacent words in a document. 
# Use the first two words of the set as a key, and remember the fact that the third word followed that key
# For this kata, try implementing a trigram algorithm that generates a couple of hundred words of text using a book-sized file as input

import random
import sys

# load sample text - sherlock holmes book
#file = open('sample_text.txt', 'r')

# read the file line by line and append each line to the end of the list.
# stripping the newline character:
# with open('filename') as f:
#    lines = f.readlines()
#file_lines = [file_lines.replace('\n', ' ') for file_lines in open('sample_text_small.txt')]
file_lines = [file_lines.replace('\n', ' ') for file_lines in open('sample_text.txt')]



# combine list seperated by lines into one big list

file_as_string = ''
for listline in file_lines:
    file_as_string = file_as_string + listline

# get rid of caps
file_as_string = file_as_string.lower()
# get rid of non word chars
file_as_string = file_as_string.replace(',','').replace('.','').replace('?', '').replace('!', '').replace('--', ' ').replace('\\', '').replace('}', '').replace('{', '')


# turn the string into a list, each item being a word
list_by_words = file_as_string.split(' ')  



t_dict = {}
# now make the trigram dictionary 
for i in range(0, len(list_by_words)-2):
    t_dict.update( [(list_by_words[i]+ ' ' + list_by_words[i+1], list_by_words[i+2] )] )

# if the dict value does not exist, instead of erroring, choose the word 'a'
default = 'a'

# start out with a random seed, this will start the sentence
pair = random.choice(list(t_dict.keys()))

sentence = pair

for i in range(200):
    # new_word = t_dict[pair]
    new_word = t_dict.get(pair, default)
    sentence = sentence + ' ' + new_word #(random.choice(followers))
    #print(sentence)
    pair_list = pair.split(' ') 
    pair = pair_list[1] + ' ' + new_word
    #print(pair)

print(sentence)


