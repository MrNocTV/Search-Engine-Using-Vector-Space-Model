import re
import string

string.punctuation += '”“'
def tokenize(data):
    data = [x.strip() for x in data.split()]
    words = []
    for token in data:
        if token[0] in string.punctuation:
            token = token[1:]
        while len(token) > 0 and token[-1] in string.punctuation:
            token = token[:-1]
        if len(token) > 1:
            if re.match(r'\w+[/]\w+', token):
                token = re.sub(r'/', ' ', token)
                token = token.split()
                words.append(token[0].lower())
                words.append(token[1].lower())
            else:
                words.append(token.lower())

    print(*words, sep='\n')
            

tokenize(open('/home/loctv/Documents/Python/IR-Remake/data/TTO_050812_0637.txt').read())