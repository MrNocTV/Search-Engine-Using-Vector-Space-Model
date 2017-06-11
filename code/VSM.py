from utils import term_frequency
from utils import tokenize, remove_stop_words
from collections import defaultdict
from itertools import combinations
import os
import MySQLdb
import math
import time

doc_folder = '/home/loctv/Documents/Python/IR-Remake/news'

def connect_server(config_file='config.txt'):
    config_dict = eval(open(config_file).read().strip())
    host = config_dict['host']
    user = config_dict['user']
    passwd = config_dict['passwd']
    db = config_dict['db']

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset='utf8')
    return db
    
def preprocessing_and_indexing(doc_folder=doc_folder):
    bag_of_word = {}
    total_docs = 0
    print("start indexing")
    start = time.time()
    db = connect_server()   
    cur = db.cursor()
    cur.execute('TRUNCATE TABLE term;')
    cur.execute('TRUNCATE TABLE entry;')
    cur.execute('TRUNCATE TABLE doc;')
    
    
    count = 0
    for file_name in os.listdir(doc_folder):
        count += 1
        file_path = os.path.join(doc_folder, file_name)
        total_docs += 1
        
        content = open(file_path, encoding='utf16').read().strip()
        # -- preprocessing --
        token = tokenize(content)
        length = len(list(token))
        list_word = token
        token = remove_stop_words(token)
        # -------------------
        counter = term_frequency(token)
        cur.execute('INSERT INTO doc (title, content, length) VALUES (%s, %s, %s)', [file_name, os.path.join(doc_folder, file_name), length])
        for word in counter:
            if word in bag_of_word:
                bag_of_word[word][file_name] = counter[word]
            else:
                bag_of_word[word] = {}
                bag_of_word[word][file_name] = counter[word]
        if count % 1000 == 0:
            print(count)
    # bag_of_word (dict of dict) looks like:
    # word1:doc1 = 1
    # word1:doc2 = 2 
    # word2:doc1 = 3
    # ... 
    print('Dumping term, entry')
    count = 1
    print("need to dump {} words".format(len(bag_of_word)))
    for word in bag_of_word:
        # with each word calculate it's idf 
        idf = 1 + math.log(total_docs / len(bag_of_word[word]))
        cur.execute('INSERT INTO term (content, idf) VALUES (%s, %s)', [word, idf])
        # traverse through all docs that contain it 
        # calculate word's df inside each doc 
        for file_name in bag_of_word[word]:
            tf = bag_of_word[word][file_name]
            cur.execute('INSERT INTO entry (doc, term, tf) VALUES (%s, %s, %s)', [file_name, count, tf])
        if count % 1000 == 0:
            print(count)
        count += 1
    db.commit()
    db.close()
    print("Finish indexing")
    print("Took {} second".format(time.time()-start))

def querying_and_ranking(query, cur):
    # -- preprocessing query --
    print("process query")
    query = process_query(query, cur)
    query_id = []
    for word in query:
        cur.execute("SELECT id, content FROM term WHERE content=%s", [word])
        for id, content in cur.fetchall():
            if content == word:
                query_id.append(id)
                break 
    print(query_id)
    if len(query) < 2:
        return None 
    # with each word, find out the docs containing it 
    word_docs = defaultdict(dict)
    for word in query_id:
        cur.execute("SELECT doc,term.content,tf from entry JOIN term ON term.id=%s AND entry.term=term.id", [word])
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            doc, term, tf = row
            word_docs[word][doc] = tf
    # example of word_docs
    # {1[doc2.txt] = 1, 1[doc1.txt] = 1, 
    # 2[doc1.txt] = 1, 2[doc3.txt] = 1}
    # this is not what we want, we want its backward 
    # doc is key and word is value 
    # so that we can instantly know all words (from query) that a doc has 
    # 'doc2.tx : [(1, 1)]
    # 'doc1.txt' : [(2, 1), (1, 1)]
    # 'doc3.txt' : [(2, 1)]
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
    for word in query_id:
        cur.execute('SELECT content, idf from term WHERE term.id=%s', [word])
        rows = cur.fetchall()
        content, idf = rows[0] 
        word_idf[word] = idf 
    # print(doc_words)
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
    for i in range(len(query_id)):
        tf = query.count(query[i])
        tf = tf / len(query)
        idf = word_idf[query_id[i]]
        tf_idf = tf * idf
        query_words[query_id[i]]['tf_idf'] = tf_idf
    print("calculating cosin")
    results = []
    # print(word_docs)
    for file_name in doc_words:
        cos, matches = cosin_similarity(doc_words[file_name], query_words, file_name)
        results.append((file_name, cos, matches))
    # get first 100 docs
    results = list(sorted(results, key= lambda x: x[1], reverse=True))[:100]
    print("Done")
    # reranking
    # base on results of VSM, we can improve the result 
    # with some simple methods 
    results = reranking(results, query, cur)
    return results, query

def cosin_similarity(doc, query, docname):
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
        doc_sqrt += doc[word]**2
    doc_sqrt = math.sqrt(doc_sqrt)
    
    # ||query|\
    query_sqrt = 0
    for word in query:
        query_sqrt += query[word]['tf_idf']**2
    query_sqrt = math.sqrt(query_sqrt)

    cosin = product / (doc_sqrt*query_sqrt)
    return cosin, len(doc) 

def process_query(query, cur):
    # tokenize
    query = tokenize(query)
    # remove duplicate without changing the order of words 
    without_duplicate = []
    for word in query:
        if word not in without_duplicate:
            without_duplicate.append(word)
    query = without_duplicate
    # remove word that are not in database 
    without_redundance = []
    for word in query:
        cur.execute('SELECT content FROM term WHERE content=%s', [word])
        terms = cur.fetchall()
        if len(terms) > 0:
            for term in terms:
                if term[0] == word:
                    without_redundance.append(word)
                    break
    query = without_redundance
    print(query)
    return query

def reranking(results, query, cur):
    '''
        file-name, cos, matches
    '''
    temp = []
    for doc, cos, match in results:
        adding_score = 0
        if compare_title_with_query(doc, query, cur):
            adding_score = 100
        n_grams = []
        cur.execute('SELECT content FROM doc where title=%s', [doc])
        doc_link = cur.fetchall()[0][0]
        content = open(doc_link, encoding='utf16').read()
        content = ' '.join(tokenize(content))
        for i in range(2, len(query)+1):
            terms = combinations(query, i)
            for term in terms:
                n = len(term)
                term = ' '.join(term)
                if term in content:
                    adding_score += n
                    n_grams.append(term)
        temp.append((doc, cos+adding_score, match))
        # print(adding_score)
    temp = list(sorted(temp, key= lambda x:x[1], reverse=True))
    # print(*temp, sep='\n')
    return temp

def compare_title_with_query(doc, query, cur):
    cur.execute('SELECT content from doc where title=%s', [doc])
    link_content = cur.fetchall()[0][0]
    title = open(link_content, encoding='utf16').readlines()[0].strip()
    title = ' '.join(tokenize(title))
    query = ' '.join(query) 
    return query in title
    


if __name__ == '__main__':
    preprocessing_and_indexing()