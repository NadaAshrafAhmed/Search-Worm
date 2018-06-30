from collections import defaultdict

import pandas as pd
from surprise import Reader, Dataset, KNNBasic, accuracy
from surprise.model_selection import KFold
from db import *

import json



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


# TODO: save wordsID, rating dict in collaborative table
# TODO: save wordfreq in user table
def calc_collaborative_param(new_words, id):

    ratings_dict = select_ratings_dic()

    print("ratings dic")
    print(ratings_dict)


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

    ratings_dict = select_ratings_dic()

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

    global top_n
    top_n = get_top_n(predictions, n=3)

    with open('top_n.json', 'w') as fp:
        json.dump(top_n, fp, indent=4)

    return top_n


def get_suggested_URLs(id):
    new_words = []

    # for all users get item id
    # for uid, user_ratings in top_n.items():
    #     print(uid, [iid for (iid, _) in user_ratings])
    with open('top_n.json', 'r') as fp:
        top_n = json.load(fp)

    new_items = top_n[id]
    for iid, _ in new_items:
        for word, wid in wordsIDs.items():
            if wid == iid:
                new_words.append(word)
    print("suggested URLs")
    print(new_words)

    return new_words
