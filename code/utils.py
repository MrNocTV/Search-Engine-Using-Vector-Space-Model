# for utility functions 
import re
import string
import math
from collections import Counter

string.punctuation += '”“'
def tokenize(data):
    data = [x.strip() for x in data.split()]
    words = []
    for token in data:
        if token[0] in string.punctuation:
            token = token[1:]
        while len(token) > 0 and token[-1] in string.punctuation:
            token = token[:-1]
        if len(token) > 0:
            # some words are special 
            # like dacam/dioxin 
            # the solution here is to split them into two words 
            # and save both of them 
            if re.match(r'[A-Za-z]+[/][A-Za-z]+', token):
                token = re.sub(r'/', ' ', token)
                token = token.split()
                words.append(token[0].lower())
                words.append(token[1].lower())
            else:
                words.append(token.lower())

    return words 

def remove_too_long_stop_words():
    '''
        Remove stop words that have more than 2 words 
        inside stop_words.txt
    '''
    stop_words = set()
    # first get all stop word 
    # remove if they can split into two words 
    with open('/home/loctv/Documents/Python/IR-Remake/stop_word/stop_words.txt') as f:
        for line in f:
            if len(line.split()) == 1:
                stop_words.add(line.strip())
    # then override the 1-word stop words into the file 
    with open('/home/loctv/Documents/Python/IR-Remake/stop_word/stop_words.txt', 'w') as f:
        for stop_word in stop_words:
            f.write(stop_word + '\n')


def remove_stop_words(data):
    result = []
    stop_words = set(word.strip() for word in open('/home/loctv/Documents/Python/IR-Remake/stop_word/stop_words.txt').readlines())
    for word in data:
        if word not in stop_words:
            yield word 

def term_frequency(doc):
    # counting
    freq = Counter(doc)
    return dict(freq)

def inverse_document_frequency(total_doc, doc_contain_word):
    return 1 + math.log(total_doc / doc_contain_word)

if __name__ == '__main__':
    # data = tokenize(open('/home/loctv/Documents/Python/IR-Remake/news/TTO_050812_0637.txt').read())
    # for word in remove_stop_words(data):
    #     print(word)
    print(term_frequency(open('/home/loctv/Documents/Python/IR-Remake/testing_data/doc3.txt').read().split()))
    print('IDF(game) = {}'.format(inverse_document_frequency(3, 1)))