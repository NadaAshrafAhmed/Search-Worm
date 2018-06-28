import codecs
import contextlib

import pickle
from flask import Flask, render_template, request, json

from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans

import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

import gensim
from gensim import corpora

from googlesearch import search

from collections import defaultdict

from surprise import Reader, Dataset, accuracy

from surprise import KNNBasic
from surprise.model_selection import KFold

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
all_topics = []

# changeable for each use   r
id = 2
new_words = []
wordFreq = defaultdict(dict)  # must read all previous frequencies for user X

# global for all users
wordsIDs = defaultdict(dict)
ratings_dict = {'itemID': list(),
                'userID': list(),
                'rating': list()}

top_n = defaultdict(list)


def write_wid_dic():
    file = open('wid-dic.txt', 'a+')
    file.write(str(wordsIDs.__len__()))
    file.write('\n')
    for word, id in wordsIDs.items():
        file.write(word)
        file.write(' ')
        file.write(str(id))
        file.write('\n')

    file.write('\n')
    for item in ratings_dict['itemID']:
        file.write(str(item))
        file.write(' ')
    file.write('\n')
    for user in ratings_dict['userID']:
        file.write(str(user))
        file.write(' ')
    file.write('\n')
    for rate in ratings_dict['rating']:
        file.write(str(rate))
        file.write(' ')
    file.write('\n')
    file.close()


def read_wid_dic():
    file = open('wid-dic.txt', 'r')
    len = int(file.readline())
    for i in range(0, len):
        w_id = file.readline().split()
        wordsIDs[w_id[0]] = int(w_id[1])

    ratings_dict['itemID'] = file.readline().strip('\n').split(' ')
    ratings_dict['userID'] = file.readline().strip('\n').split(' ')
    ratings_dict['rating'] = file.readline().strip('\n').split(' ')

    for i in range(0, ratings_dict['itemID'].__len__()):
        ratings_dict['itemID'][i] = int(ratings_dict['itemID'][i])

    for i in range(0, ratings_dict['userID'].__len__()):
        ratings_dict['userID'][i] = int(ratings_dict['userID'][i])

    for i in range(0, ratings_dict['rating'].__len__()):
        ratings_dict['rating'][i] = float(ratings_dict['rating'][i])

    file.close()


def calc_collaborative_param():
    for word in new_words:
        if word not in wordsIDs:
            wordsIDs[word] = wordsIDs.__len__()
        if word in wordFreq:
            wordFreq[word] += 1
        else:
            wordFreq[word] = 1

    print("Words freq")
    print(wordFreq)
    print("Words ID")
    print(wordsIDs)


def get_top_n(predictions, n):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    print("get top n")
    # First map the predictions to each user.
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def collaborative_filter():
    # edit ratings dict
    mx = sum(wordFreq.values())
    global new_words
    new_words = list(set(new_words))
    for word in new_words:
        ratings_dict['rating'].append(float(wordFreq[word]) / mx * 5)  # normalized
        ratings_dict['itemID'].append(wordsIDs[word])
        ratings_dict['userID'].append(id)

    print("rating dict")
    print(ratings_dict)
    df = pd.DataFrame(ratings_dict)

    # A reader is still needed but only the rating_scale param is required.
    reader = Reader(rating_scale=(0.0, 5.0))
    # The columns must correspond to user id, item id and ratings (in that order).
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
    # define a cross-validation iterator
    kf = KFold(n_splits=3)

    algo = KNNBasic()

    for trainset, testset in kf.split(data):
        # train and test algorithm.
        algo.fit(trainset)
        kf_predictions = algo.test(testset)
        # Compute and print Root Mean Squared Error
        accuracy.rmse(kf_predictions, verbose=True)

    trainset = data.build_full_trainset()

    new_data = trainset.build_anti_testset()
    predictions = algo.test(new_data)
    get_top_n(predictions, n=3)


def get_suggested_URLs():
    new_items_words = []

    # for all users get item id
    # for uid, user_ratings in top_n.items():
    #     print(uid, [iid for (iid, _) in user_ratings])

    new_items = top_n.get(id)
    for iid, _ in new_items:
        for word, wid in wordsIDs.iteritems():
            if wid == iid:
                new_items_words.append(word)


def k_means():
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(documents)

    # vectorizer.get_feature_names()

    # print(X.toarray())

    transformer = TfidfTransformer(smooth_idf=False)
    tfidf = transformer.fit_transform(X)
    # print(tfidf.shape)

    num_clusters = 4  # Change it according to your data.
    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf)
    c = km.labels_.tolist()

    for i in c:
        clusters.append(i)

        # idea = {'Idea': documents, 'Cluster': clusters}  # Creating dict having doc with the corresponding cluster number.
        # frame = pd.DataFrame(idea, index=[clusters], columns=['Idea', 'Cluster'])  # Converting it into a dataframe.
        #
        # print("\n")
        # print(frame)  # Print the doc with the labeled cluster number.
        # print("\n")
        # print(frame['Cluster'].value_counts())  # Print the counts of doc belonging to each cluster.

        # print("Top terms per cluster:")
        # order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        # terms = vectorizer.get_feature_names()
        # for i in range(num_clusters):
        #     print("Cluster %d:" % i, )
        #     for ind in order_centroids[i, :10]:
        #         print(' %s' % terms[ind], )
        #     print()

        # save to disk, not sure if we need it (small size!)
        # filename = 'finalized_model.sav'
        # pickle.dump(km, open(filename, 'wb'))

        # plotting for presentation (not working, yet!)

        # pca = PCA(n_components=4).fit(X)
        # centers2D = pca.transform(km.cluster_centers_)
        #
        # plt.hold(True)
        # plt.scatter(centers2D[:, 0], centers2D[:, 1],
        #             marker='x', s=200, linewidths=3, c='r')
        # plt.show()  # not required if using ipython notebook


def clean(doc):
    doc = re.sub("[^a-zA-Z0-9\s\\n]", " ", doc)
    doc = re.sub("\\s+", " ", doc)

    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def LDA(doc_complete, n):
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

    for i in range(0, 3):
        topn_words = [word for word, prob in ldamodel.show_topic(i, topn=3)]

        if n == 1:
            topic_words1.append(topn_words)
        elif n == 2:
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


# def history1():
#     # return str({str(["a","b","c","d"]),str(["e","f","g","h"]),str(["i","j","k","l"]),str(["m","n","o","p"])}).replace("'", '"')
#     return str([["a","b","c","d"],["e","f","g","h"],["i","j","k","l"],["m","n","o","p"]]).replace("'", '"')
@app.route('/history', methods=["POST"])
def history():
    # list of user history
    urls = list(set(request.get_json()['urls']))
    # id = request.get_json()['ID']
    read_wid_dic()
    print("Reading URLS")
    for url in urls:
        # print(url)
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

                doc = clean(doc)  # better accuracy for k-means

                documents.append(doc)
                # print(doc)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
    print("Starting k-means")
    k_means()

    for i in range(0, len(clusters)):

        if clusters[i] == 0:
            topic1.append(documents[i])

        elif clusters[i] == 1:
            topic2.append(documents[i])

        elif clusters[i] == 2:
            topic3.append(documents[i])

        elif clusters[i] == 3:
            topic4.append(documents[i])

    LDA_results_file = open('LDA-results.txt', 'a+')

    if len(topic1) > 0:

        LDA(topic1, 1)

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
            all_topics.append(i)
            for j in i:
                k = 0
                LDA_results_file.write(j)
                LDA_results_file.write(' ')
                new_words.append(j)
                try:
                    res = search(j, stop=3)
                    for r in res:
                        if k < 3:
                            urls1.append(r)
                            k += 1
                except Exception as e:
                    print(e)
            LDA_results_file.write('\n')
    if len(topic2) > 0:

        LDA(topic2, 2)

        for i in topic_words2:
            all_topics.append(i)
            for j in i:
                k = 0
                LDA_results_file.write(j)
                LDA_results_file.write(' ')
                new_words.append(j)
                try:
                    res = search(j, stop=3)
                    for r in res:
                        if k < 3:
                            urls2.append(r)
                            k += 1
                except Exception as e:
                    print(e)
            LDA_results_file.write('\n')

    if len(topic3) > 0:

        LDA(topic3, 3)

        for i in topic_words3:
            all_topics.append(i)
            for j in i:
                k = 0
                LDA_results_file.write(j)
                LDA_results_file.write(' ')
                new_words.append(j)
                try:
                    res = search(j, stop=3)
                    for r in res:
                        if k < 3:
                            urls3.append(r)
                            k += 1
                except Exception as e:
                    print(e)
            LDA_results_file.write('\n')

    if len(topic4) > 0:

        LDA(topic4, 4)

        for i in topic_words4:
            all_topics.append(i)
            for j in i:
                k = 0
                LDA_results_file.write('j')
                LDA_results_file.write(' ')
                new_words.append(j)
                try:
                    res = search(j, stop=3)
                    for r in res:
                        if k < 3:
                            urls4.append(r)
                            k += 1
                except Exception as e:
                    print(e)
            LDA_results_file.write('\n')

    LDA_results_file.close()
    calc_collaborative_param()

    url1 = list(set(urls1))
    url2 = list(set(urls2))
    url3 = list(set(urls3))
    url4 = list(set(urls4))

    print("topic1")
    print(str(len(topic_words1)))
    print(topic_words1)
    # for i in urls1:
    #     print(i)

    print("topic2")
    print(str(len(topic_words2)))
    print(topic_words2)
    # for i in urls2:
    #     print(i)

    print("topic3")
    print(str(len(topic_words3)))
    print(topic_words3)
    # for i in urls3:
    #     print(i)

    print("topic4")
    print(str(len(topic_words4)))
    print(topic_words4)
    # for i in urls4:
    #     print(i)

    all_urls.append(url1)
    all_urls.append(url2)
    all_urls.append(url3)
    all_urls.append(url4)

    all_urls_str = str(all_urls)

    all_urls_str = all_urls_str.replace("'", '"')
    print("calculating param")
    calc_collaborative_param()
    print("Start filter")
    collaborative_filter()
    print("suggested URLS")
    get_suggested_URLs()

    write_wid_dic()

    return all_urls_str


@app.route('/save_data', methods=["POST"])
def save_data():
    id = request.form.get('id')
    # print(id)

    return "Thank you !"


@app.route('/id_exist', methods=["POST"])
def id_exist():
    # id = request.get_json()['ID']
    id = 3
    # print(id)

    # check database ..

    return ("true")


if __name__ == '__main__':
    app.run(debug=True)
