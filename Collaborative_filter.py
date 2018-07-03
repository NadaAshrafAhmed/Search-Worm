import pandas as pd
from surprise import Reader, Dataset, KNNBasic, accuracy
from surprise.model_selection import KFold
from DataBase import *
from json import load, dump

wordFreq = defaultdict(dict)  # must read all previous frequencies for user X

# global for all users
ratings_dict = {'itemID': list(),
                'userID': list(),
                'rating': list()}


def calc_collaborative_param(new_words, id):
    ratings_dict = select_ratings_dic()
    wordFreq = select_user_words(id)
    wordsIDs = select_words()

    mx = sum(wordFreq.values())
    for word in new_words:
        ratings_dict['rating'].append(float(wordFreq[word]) / mx * 5)  # normalized
        ratings_dict['itemID'].append(wordsIDs[word])
        ratings_dict['userID'].append(id)

    insert_ratings_dic(ratings_dict)

    return ratings_dict


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

    top_n = defaultdict(list)

    # First map the predictions to each user.
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def collaborative_filter(id, new_words):
    ratings_dict = calc_collaborative_param(new_words, id)

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

    top_n = get_top_n(predictions, n=3)

    with open('top_n.json', 'w') as fp:
        dump(top_n, fp, indent=4)

    return top_n


def get_suggested_topics(id):
    new_words = []
    wordsIDs = select_words()
    # for all users get item id
    # for uid, user_ratings in top_n.items():
    #     print(uid, [iid for (iid, _) in user_ratings])

    try:
        with open('top_n.json', 'r') as fp:
            top_n = load(fp)

    except:
        "no new suggestions for you :( "

    new_items = top_n[id]
    for iid, _ in new_items:
        for word, wid in wordsIDs.items():
            if wid == iid:
                new_words.append(word)

    topics = select_topics()
    top_topics = []

    k = 0
    for query in topics:
        for word in query:
            for new_word in new_words:
                if word == new_word and k < 4:
                    top_topics.append(query)
                    k += 1


    interests = ["Technology", "Space", "Music", "Sports", "Nature and Animals",
                 "Science", "Fashion", "Programming", "Education", "Movies"]
    google_one_word = []

    for word in new_words:
        if word in interests:
            google_one_word.append(word)


    return top_topics, google_one_word
