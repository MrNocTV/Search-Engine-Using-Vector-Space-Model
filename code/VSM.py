from utils import term_frequency, inverse_document_frequency
from utils import tokenize, remove_stop_words
import os

doc_folder = '/home/loctv/Documents/Python/IR-Remake/testing_data'

def indexing(doc_folder=doc_folder):
    bag_of_word = {}
    for file_name in os.listdir(doc_folder):
        file_path = os.path.join(doc_folder, file_name)
        token = tokenize(open(file_path).read())
        token = remove_stop_words(token)
        counter = term_frequency(token)
        for word in counter:
            if word in bag_of_word:
                bag_of_word[word][file_name] = counter[word]
            else:
                bag_of_word[word] = {}
                bag_of_word[word][file_name] = counter[word]
    print(bag_of_word)
        
        

if __name__ == '__main__':
    indexing()


