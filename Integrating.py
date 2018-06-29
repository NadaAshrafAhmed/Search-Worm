import codecs
import contextlib

from flask import Flask, render_template, request, json
# import urllib.request
from Collaborative_filter import *

from urllib.request import Request, urlopen

import re
from bs4 import BeautifulSoup

from Clustering import k_means

from TopicModelling import LDA, clean

import glob
import os
import re
import math

import db

from googlesearch import search

app = Flask(__name__)

# k is 4

documents = []
clusters = []

topic1 = []
topic2 = []
topic3 = []
topic4 = []

topic_words1 = []
topic_words2 = []
topic_words3 = []
topic_words4 = []

urls1 = []
urls2 = []
urls3 = []
urls4 = []

all_urls = []

new_words = []


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def history1():
    return str([["a", "b", "c", "d"], ["e", "f", "g", "h"], ["i", "j", "k", "l"], ["m", "n", "o", "p"]]).replace("'",
                                                                                                                 '"')


def get_recommendations(urls, id):
    for url in urls:

        print(url)
        # req = Request(url, headers={'User-Agent': 'Mozilla/5.0'} )
        # mybytes = urlopen( req ).read()
        # mystr = mybytes.decode( "utf8" )
        # # print (mystr)
        # doc =  html2text.html2text( str( mystr ) )

        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with contextlib.closing(urlopen(req)) as webpage:
                html = webpage.read()
                html = html.decode("UTF-8")
            # html = urlopen(req)
            try:
                soup = BeautifulSoup(html, "html.parser")
                data = soup.findAll(text=True)

                result = filter(visible, data)

                arr = list(result)

                doc = ""

                for i in arr:
                    doc += i
                    doc += " "

                doc = clean(doc)

                documents.append(doc)

                print(doc)

            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    clusters = k_means(documents)

    for i in range(0, len(clusters)):

        if clusters[i] == 0:
            topic1.append(documents[i])

        elif clusters[i] == 1:
            topic2.append(documents[i])

        elif clusters[i] == 2:
            topic3.append(documents[i])

        elif clusters[i] == 3:
            topic4.append(documents[i])

    if len(topic1) > 0:

        topic_words1 = LDA(topic1)

        for i in topic_words1:
            db.add_topic(i[0], i[1], i[2])
            for j in i:
                new_words.append(j)
                k = 0
                try:
                    res = search(j, stop=3)
                    for r in res:
                        if k < 3:
                            urls1.append(r)
                            k += 1
                except Exception as e:
                    print(e)

    if len(topic2) > 0:

        topic_words2 = LDA(topic2)

        for i in topic_words2:
            db.add_topic(i[0], i[1], i[2])
            for j in i:
                k = 0
                new_words.append(j)
                try:
                    res = search(j, stop=3)
                    for r in res:
                        if k < 3:
                            urls2.append(r)
                            k += 1
                except Exception as e:
                    print(e)

    if len(topic3) > 0:

        topic_words3 = LDA(topic3)

        for i in topic_words3:
            db.add_topic(i[0], i[1], i[2])
            for j in i:
                k = 0
                new_words.append(j)
                try:
                    res = search(j, stop=3)
                    for r in res:
                        if k < 3:
                            urls3.append(r)
                            k += 1
                except Exception as e:
                    print(e)

    if len(topic4) > 0:

        topic_words4 = LDA(topic4)

        for i in topic_words4:
            db.add_topic(i[0], i[1], i[2])
            for j in i:
                k = 0
                new_words.append(j)
                try:
                    res = search(j, stop=3)
                    for r in res:
                        if k < 3:
                            urls4.append(r)
                            k += 1
                except Exception as e:
                    print(e)

    db.add_word(id, topic_words1[0] + topic_words1[1] + topic_words1[2]
                + topic_words2[0] + topic_words2[1] + topic_words2[2]
                + topic_words3[0] + topic_words3[1] + topic_words3[2]
                + topic_words4[0] + topic_words4[1] + topic_words4[2])

    url1 = list(set(urls1))
    url2 = list(set(urls2))
    url3 = list(set(urls3))
    url4 = list(set(urls4))

    print("topic1")
    print(str(len(topic_words1)))
    print(topic_words1)
    for i in urls1:
        print(i)

    print("topic2")
    print(str(len(topic_words2)))
    print(topic_words2)
    for i in urls2:
        print(i)

    print("topic3")
    print(str(len(topic_words3)))
    print(topic_words3)
    for i in urls3:
        print(i)

    print("topic4")
    print(str(len(topic_words4)))
    print(topic_words4)
    for i in urls4:
        print(i)

    calc_collaborative_param(new_words, id)
    # TODO: start filter whenever new user comes in
    collaborative_filter()
    get_suggested_URLs(id)

    all_urls.append(url1)
    all_urls.append(url2)
    all_urls.append(url3)
    all_urls.append(url4)

    all_urls_str = str(all_urls)

    all_urls_str = all_urls_str.replace("'", '"')

    return all_urls_str
