# This file is used for loading news_dataset into this project 
import os

src_folder = '/home/loctv/Downloads/news_dataset'
dst_folder = '../news'

def copy_file(src, dst, N):
    '''
        src: directory contains only .txt file 
        dst: destination folder 
        load N files from news_dataset into news
    '''
    count = 0
    for filename in os.listdir(src)[:N]:
        src_file = os.path.join(src, filename)
        dst_file = os.path.join(dst, 'd' + str(count) + '.txt')
        count += 1
        src_file = open(src_file, encoding='utf-16')
        dst_file = open(dst_file, 'w')
        for line in src_file:
            dst_file.write(line.strip() + '\n')
        src_file.close()
        dst_file.close()

copy_file(src_folder, dst_folder, 10)