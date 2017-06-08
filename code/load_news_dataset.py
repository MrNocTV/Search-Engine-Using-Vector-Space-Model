import os

src_folder = '/home/loctv/Downloads/news_dataset'
dst_folder = '../data'

def copy_file(src, dst):
    '''
        src: directory contains only .txt file 
        dst: destination folder 
    '''
    for filename in os.listdir(src)[:10]:
        src_file = os.path.join(src, filename)
        dst_file = os.path.join(dst, filename)
        src_file = open(src_file, encoding='utf-16')
        dst_file = open(dst_file, 'w')
        for line in src_file:
            dst_file.write(line.strip() + '\n')
        src_file.close()
        dst_file.close()

copy_file(src_folder, dst_folder)