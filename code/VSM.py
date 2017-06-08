from utils import term_frequency, inverse_document_frequency
from utils import tokenize, remove_stop_words
import os
import MySQLdb
import math

doc_folder = '/home/loctv/Documents/Python/IR-Remake/testing_data'

def connect_server(config_file='config.txt'):
    config_dict = eval(open(config_file).read().strip())
    host = config_dict['host']
    user = config_dict['user']
    passwd = config_dict['passwd']
    db = config_dict['db']

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    return db
    
def indexing(doc_folder=doc_folder):
    bag_of_word = {}
    total_docs = 0
    db = connect_server()   
    cur = db.cursor()
    cur.execute('TRUNCATE TABLE doc;')
    cur.execute('TRUNCATE TABLE term;')
    cur.execute('TRUNCATE TABLE entry;')
    for file_name in os.listdir(doc_folder):
        file_path = os.path.join(doc_folder, file_name)
        total_docs += 1
        content = open(file_path).read().strip()
        # -- preprocessing --
        token = tokenize(content)
        length = len(list(token))
        token = remove_stop_words(token)
        # -------------------
        counter = term_frequency(token)
        cur.execute('INSERT INTO doc (title, content, length) VALUES (%s, %s, %s)', [file_name, content, length])
        for word in counter:
            if word in bag_of_word:
                bag_of_word[word][file_name] = counter[word]
            else:
                bag_of_word[word] = {}
                bag_of_word[word][file_name] = counter[word]
    for term in bag_of_word:
        idf = 1 + math.log(total_docs / len(bag_of_word[term]))
        cur.execute('INSERT INTO term (content, idf) VALUES (%s, %s)', [term, idf])
        for file_name in bag_of_word[term]:
            df = len(bag_of_word[term])
            cur.execute('INSERT INTO entry (doc, term, df) VALUES (%s, %s, %s)', [file_name, term, df])
    db.commit()
    db.close()

if __name__ == '__main__':
    indexing()


