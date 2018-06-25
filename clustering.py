import codecs

from flask import Flask, render_template, request, json
# import urllib.request
import html2text

from urllib.request import Request, urlopen

import re
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans

import glob
import os
import re
import math
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

import gensim
from gensim import corpora

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

def k_means():


    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(documents)

    # vectorizer.get_feature_names()

    # print(X.toarray())

    transformer = TfidfTransformer(smooth_idf=False)
    tfidf = transformer.fit_transform(X)
    print(tfidf.shape)

    num_clusters = 4 # Change it according to your data.
    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf)
    c = km.labels_.tolist()

    for i in c:
        clusters.append(i)

    idea = {'Idea': documents, 'Cluster': clusters}  # Creating dict having doc with the corresponding cluster number.
    frame = pd.DataFrame(idea, index=[clusters], columns=['Idea', 'Cluster'])  # Converting it into a dataframe.

    print("\n")
    print(frame)  # Print the doc with the labeled cluster number.
    print("\n")
    print(frame['Cluster'].value_counts())  # Print the counts of doc belonging to each cluster.

    # return "7mada"


def clean(doc):

    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def LDA( doc_complete , n ):

    doc_clean = [clean(doc).split() for doc in doc_complete]

    '''Topic modeling'''

    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=3, id2word=dictionary, passes=50)

    arr = ldamodel.print_topics(num_topics=3, num_words=3)

    for i in range(0,3):
        topn_words = [word for word, prob in ldamodel.show_topic(i, topn=3)]

        if n==1 :
            topic_words1.append(topn_words)
        elif n==2 :
            topic_words2.append(topn_words)
        elif n == 3:
            topic_words3.append(topn_words)
        elif n == 4:
            topic_words4.append(topn_words)



    # for i in topic_words1:
    #     print(i)



def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


@app.route('/history',methods=["POST"])
def history1():
    # return str({str(["a","b","c","d"]),str(["e","f","g","h"]),str(["i","j","k","l"]),str(["m","n","o","p"])}).replace("'", '"')
    return str([["a","b","c","d"],["e","f","g","h"],["i","j","k","l"],["m","n","o","p"]]).replace("'", '"')

def history():
    # list of user history
    urls=request.get_json()['urls']
    id = request.get_json()['ID']
    print(id)

    for url in urls:
        print( url )
        # req = Request(url, headers={'User-Agent': 'Mozilla/5.0'} )
        # mybytes = urlopen( req ).read()
        # mystr = mybytes.decode( "utf8" )
        # # print (mystr)
        # doc =  html2text.html2text( str( mystr ) )

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        soup = BeautifulSoup(html,"html.parser")
        data = soup.findAll(text=True)

        result = filter(visible, data)

        arr = list(result)

        doc = ""

        for i in arr:
            doc += i
            doc += "\n"

        documents.append(doc)
        print( doc )

    k_means()

    for i in range(0,len(clusters)):

        if clusters[i]==0:
            topic1.append(documents[i])

        elif clusters[i]==1:
            topic2.append(documents[i])

        elif clusters[i]==2:
            topic3.append(documents[i])

        elif clusters[i]==3:
            topic4.append(documents[i])

    if len(topic1)>0:

        LDA(topic1,1)

        # c=0
        #
        # print(topic_words1[0][0])
        #
        # res = search("python",stop= 3)
        # print("af res")
        # for i in res:
        #     print(i)
        #     c += 1
        #
        # print("c:   " + str(c))

        for i in topic_words1:
            for j in i :
                print(j)
                k = 0
                res = search(j,stop= 3)
                for r in res:
                    if k<3:
                        urls1.append(r)
                        k += 1

    if len(topic2) > 0:

        LDA(topic2,2)

        for i in topic_words2:
            for j in i :
                k = 0
                res = search(j,stop= 3)
                for r in res:
                    if k<3:
                        urls2.append(r)
                        k += 1

    if len(topic3) > 0:

        LDA(topic3,3)

        for i in topic_words3:
            for j in i :
                k = 0
                res = search(j,stop= 3)
                for r in res:
                    if k<3:
                        urls3.append(r)
                        k += 1

    if len(topic4) > 0:

        LDA(topic4,4)

        for i in topic_words4:
            for j in i :
                k=0
                res = search(j,stop= 3)
                for r in res:
                    if k<3:
                        urls4.append(r)
                        k += 1

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

    all_urls.append(urls1)
    all_urls.append(urls2)
    all_urls.append(urls3)
    all_urls.append(urls4)

    all_urls_str = str(all_urls)

    all_urls_str = all_urls_str.replace("'", '"')

    return (all_urls_str)


@app.route('/save_data',methods=["POST"])
def save_data():
    id = request.form.get('id')
    print(id)

    return "Thank you !"


@app.route('/id_exist',methods=["POST"])
def id_exist():

    id = request.get_json()['ID']
    print(id)

    #check database ..

    return ("true")

if __name__ == '__main__':
    app.run(debug=True)