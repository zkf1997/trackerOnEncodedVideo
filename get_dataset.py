# -*- coding: utf-8 -*-
import os
import time
import requests
import re
from lxml import html
from PIL import Image
from io import BytesIO
from tqdm import  tqdm

rootdir = os.path.abspath('.')
url = 'http://cvlab.hanyang.ac.kr/tracker_benchmark/datasets.html'
url_base = 'http://cvlab.hanyang.ac.kr/tracker_benchmark/'

def save(text, filename='temp', path='download'):
    fpath = os.path.join(path, filename)
    with open(fpath, 'w') as  f:
        image = Image.open(BytesIO(text))
        print('output:', fpath)
        image.save(fpath)


def save_sequence(sequence_url, data_dir):
    zip_file = sequence_url.split('/')[-1]
    sequence_name = zip_file.split('.')[0]
    cmd = 'cd ' + data_dir + " && " + \
          'axel -n 8 -o ' + data_dir + '/ ' + sequence_url + ' && ' + \
          "unzip " + zip_file + ' && ' +\
          'rm -rf ' + zip_file + ' && ' + \
          'cd ' + data_dir + '/' + sequence_name + '&&' +\
          "image_type=$(ls ./img | grep '.')" + '&&' +\
          'ffmpeg -threads 8 -y -f image2 -i ./img/%04d.${image_type##*.} -vcodec libx264 -r 30 ' + '%s.mp4' % (sequence_name)
    #${var##*.} extract the text after final '.'
    os.system(cmd)
    # os.system('axel -n 8 -o ' + data_dir + '/ ' + sequence_url)
    # os.system('ls')
    # os.system('unzip ' + zip_file)
    # os.remove(zip_file)
    # # sequence_dir = zip_file.split('.')[0]
    # # os.system('cd ' + sequence_dir)
    # #
    # os.system('cd ' + rootdir)


def crawl(url):
    resp = requests.get(url)
    page = str(resp.content)

    root = html.fromstring(page)
    sequence_urls = root.xpath('//*[@id="motion" and @class="seqtable"]//a[@href]/@href')

    if not os.path.exists(os.path.join(rootdir, 'dataset')):
        os.mkdir(os.path.join(rootdir, 'dataset'))

    if not os.path.exists(os.path.join(rootdir, 'dataset', 'OTB100')):
        os.mkdir(os.path.join(rootdir, 'dataset', 'OTB100'))

    # save_sequence(url_base + sequence_urls[0], os.path.join(rootdir, 'dataset', 'OTB100'))
    for sequence_url in tqdm(sequence_urls):
        save_sequence(url_base + sequence_url, os.path.join(rootdir, 'dataset', 'OTB100'))


if __name__ == '__main__':
    crawl(url)

