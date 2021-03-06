from  contextlib import closing
from flask import Flask
from Collaborative_filter import *
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from Clustering import k_means
from TopicModelling import LDA, clean
from re import match

import DataBase

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
urls5 = []

all_urls = []

new_words = []


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def history1():
    return str([["a", "b", "c", "d"], ["e", "f", "g", "h"], ["i", "j", "k", "l"], ["m", "n", "o", "p"]]).replace("'",
                                                                                                                 '"')
def filter_urls(urls):
    remove=['127.0.0.1','localhost',"facebook","chrome-extension"]

    removed_urls=[url for url in urls for r in remove if r in url   ]
    filtered_urls=list(set(urls)-set(removed_urls))
    return filtered_urls

def get_recommendations(urls, id):
    urls = filter_urls( urls )
    # print(urls)
    for url in urls:
        print(url)
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with closing(urlopen(req)) as webpage:
                html = webpage.read()
                html = html.decode("UTF-8")
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
            DataBase.add_topic(i[0], i[1], i[2])
            for j in i:
                new_words.append(j)

            try:
                k = 0
                res = search(' '.join( i ), stop=3)
                for r in res:
                    if k < 3:
                        urls1.append(r)
                        k += 1
            except Exception as e:
                print(e)

    if len(topic2) > 0:

        topic_words2 = LDA(topic2)

        for i in topic_words2:
            DataBase.add_topic(i[0], i[1], i[2])
            for j in i:
                new_words.append(j)
            try:
                k = 0
                res = search(' '.join( i ), stop=3)
                for r in res:
                    if k < 3:
                        urls2.append(r)
                        k += 1
            except Exception as e:
                print(e)

    if len(topic3) > 0:

        topic_words3 = LDA(topic3)

        for i in topic_words3:
            DataBase.add_topic(i[0], i[1], i[2])
            for j in i:

                new_words.append(j)
            try:
                k = 0
                res = search(' '.join( i ), stop=3)
                for r in res:
                    if k < 3:
                        urls3.append(r)
                        k += 1
            except Exception as e:
                print(e)

    if len(topic4) > 0:

        topic_words4 = LDA(topic4)


        for i in topic_words4:
            DataBase.add_topic(i[0], i[1], i[2])
            for j in i:
                new_words.append( j )
            try:
                k = 0

                res = search(' '.join( i ), stop=3)
                for r in res:
                    if k < 3:
                        urls4.append(r)
                        k += 1
            except Exception as e:
                print(e)


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

    DataBase.manage_collab_param(id, new_words)
    collaborative_filter(id, new_words)
    suggested_topics, suggested_interests = get_suggested_topics(id)
    print("suggested interests")
    print(suggested_interests)

    for topic in suggested_topics:
        try:
            res = search(' '.join(topic), stop=3)
            k = 0
            for r in res:
                if k < 3:
                    urls5.append(r)
                    k += 1
        except Exception as e:
            print(e)

    for topic in suggested_interests:
        try:
            res = search(topic, stop=3)
            k = 0
            for r in res:
                if k < 3:
                    urls5.append(r)
                    k += 1
        except Exception as e:
            print(e)

    print("URLs 5 finallyy~~~")
    print(urls5)

    all_urls.append(url1)
    all_urls.append(url2)
    all_urls.append(url3)
    all_urls.append(url4)
    all_urls.append(urls5)

    all_urls_str = str(all_urls)

    all_urls_str = all_urls_str.replace("'", '"')

    return all_urls_str
