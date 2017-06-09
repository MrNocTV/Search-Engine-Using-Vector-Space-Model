from utils import term_frequency, inverse_document_frequency
from utils import tokenize, remove_stop_words
from collections import defaultdict
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
    
def preprocessing_and_indexing(doc_folder=doc_folder):
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
        list_word = token
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
    # bag_of_word (dict of dict) looks like:
    # word1:doc1 = 1
    # word1:doc2 = 2 
    # word2:doc1 = 3
    # ... 
    for word in bag_of_word:
        # with each word calculate it's idf 
        idf = 1 + math.log(total_docs / len(bag_of_word[word]))
        cur.execute('INSERT INTO term (content, idf) VALUES (%s, %s)', [word, idf])
        # traverse through all docs that contain it 
        # calculate word's df inside each doc 
        for file_name in bag_of_word[word]:
            tf = bag_of_word[word][file_name]
            cur.execute('INSERT INTO entry (doc, term, tf) VALUES (%s, %s, %s)', [file_name, word, tf])
    db.commit()
    db.close()

def querying_and_ranking(query):
    # -- preprocessing query --
    # tokenize
    query = tokenize(query)
    # remove duplicate without changing the order of words 
    without_duplicate = []
    for word in query:
        if word not in without_duplicate:
            without_duplicate.append(word)
    query = without_duplicate
    
    # -- connecting to database --
    db = connect_server()
    cur = db.cursor()
    # with each word, find out the docs containing it 
    word_docs = defaultdict(dict)
    for word in query:
        cur.execute("SELECT doc, tf from entry WHERE term=%s", [word])
        for rows in cur.fetchall():
            doc, tf = rows 
            word_docs[word][doc] = tf
    # example of word_docs
    # {life[doc2.txt] = 1, life[doc1.txt] = 1, 
    # learning[doc1.txt] = 1, learning[doc3.txt] = 1}
    # this is not what we want, we want its backward 
    # doc is key and word is value 
    # so that we can instantly know all words (from query) that a doc has 
    # 'doc2.txt' : [('life', 1)]
    # 'doc1.txt' : [('learning', 1), ('life', 1)]
    # 'doc3.txt' : [('learning', 1)]
    # -- convert key to val, val to key --
    doc_words = defaultdict(dict)
    for word in word_docs:
        for doc in word_docs[word]:
            tf =  word_docs[word][doc]
            doc_words[doc][word] = tf
    # get length for each doc
    doc_length = dict()
    for doc in doc_words:
        cur.execute('SELECT length from doc WHERE title=%s', [doc])
        length = cur.fetchall()[0][0]
        doc_length[doc] = length
    # get idf for each word in query 
    word_idf = dict()
    for word in query:
        cur.execute('SELECT idf from term WHERE content=%s', [word])
        idf = cur.fetchall()[0][0]
        word_idf[word] = idf 

    # -- querying and ranking --
    # tf*idf for words in each doc
    for doc in doc_words:
        for word in doc_words[doc]:
            tf = doc_words[doc][word]
            tf = tf / doc_length[doc]
            tf_idf = tf * word_idf[word]
            doc_words[doc][word] = tf_idf
    # tf*idf for words in query
    query_words = defaultdict(dict)
    for word in query:
        tf = query.count(word)
        tf = tf / len(query)
        idf = word_idf[word]
        tf_idf = tf * idf
        query_words[word]['tf_idf'] = tf_idf
    cosin_similarity(doc_words['doc1.txt'], query_words)

def cosin_similarity(doc, query):
    '''
        doc: dictionary, key = doc name, value = (word, idf)
        query: dictionary, key = word in query, value = (tf_idf:xxx)
    '''
    # dot product 
    product = 0
    for word in query:
        if word in doc:
            product += (query[word]['tf_idf'] * doc[word])
    # ||doc||
    doc_sqrt = 0
    for word in doc:
        if word in query:
            doc_sqrt += doc[word]**2
    doc_sqrt = math.sqrt(doc_sqrt)
    # ||query|\
    query_sqrt = 0
    for word in query:
        query_sqrt += query[word]['tf_idf']**2
    query_sqrt = math.sqrt(query_sqrt)
    cosin = product / (doc_sqrt*query_sqrt)
    print(cosin)

if __name__ == '__main__':
    preprocessing_and_indexing()
    querying_and_ranking('life learning')

