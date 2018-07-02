import mysql.connector
from collections import defaultdict

def add_user(id, name, age, nation, country, gender, interests):
    if not user_exist(id):
        db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
        cur = db.cursor()
        cur.execute("INSERT INTO user VALUES ('" + id + "', '" + name + "', '" + str(age)
                    + "', '" + nation + "', '" + country + "', '" + gender + "' );")
        cur.execute("SELECT * FROM user")
        for r in cur.fetchall():
            print(r)
        db.commit()

        cur.close()
        db.close()

    manage_user_interests(id, interests)


def user_exist(id):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    cur.execute("SELECT name FROM user WHERE id='" + id + "';")
    cur.fetchall()
    return (cur.rowcount > 0)


def manage_collab_param(user_id, words):
    add_word(user_id, words)
    insert_words(words)


def manage_user_interests(user_id, interests):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    stmt = "insert into ratings_dict (user_id, item_id, rating) values (%s, %s, %s);"
    insert_user_interest(user_id, interests)
    interestsID = select_interests_ids()

    for interest in interests:
        for i, iid in interestsID.items():
            if i == interest:
                data = (user_id, iid, 5)
                cur.execute(stmt, data)

    db.commit()
    cur.close()
    db.close()


def add_word(user_id, words):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    # cur.execute( "INSERT INTO user VALUES ('" + id + "', '" + name + "', '" + str( age ) + "', '" + nation + "');" )
    cur.execute("SELECT word, frq FROM userword WHERE user_id='" + user_id + "' ;")
    user_words = {}
    for (word, frq) in cur.fetchall():
        user_words[word] = frq
    new_words = []
    updated_words = []
    for word in words:
        if word in user_words:
            user_words[word] += 1
            updated_words.append(word)
        else:
            user_words[word] = 1
            new_words.append(word)

    new_words = list(set(new_words))
    updated_words = list(set(updated_words))

    for word in new_words:
        # cur.execute( "INSERT INTO words VALUES ('" + word + "');" )#cheak if word is uniqe or get all the words from topic or user word ana delete table words
        cur.execute("INSERT INTO userword VALUES ('" + user_id + "', '" + word + "', '1');")
    for word in updated_words:
        cur.execute("UPDATE userword SET frq='" + str(
            user_words[word]) + "' WHERE user_id= '" + user_id + "' and word= '" + word + "';")

    db.commit()
    cur.close()
    db.close()


def add_topic(w1, w2, w3):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    cur.execute("SELECT max(id) as mx FROM topic ;")
    id = 0;
    for mx in cur.fetchall():
        id = mx[0]
    if (id):
        id += 1;
    else:
        id = 1
    cur.execute("INSERT INTO topic VALUES ('" + w3 + "', '" + w1 + "', '" + w2 + "', '" + str(id) + "');")

    db.commit()
    cur.close()
    db.close()


def select_topics():
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    cur.execute("SELECT word1, word2, word3 FROM topic ;")
    topics = []
    for word1, word2, word3 in cur.fetchall():
        topics.append([word1, word2, word3])

    db.commit()
    cur.close()
    db.close()
    return topics


def select_user_words(user_id):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    # cur.execute( "INSERT INTO user VALUES ('" + id + "', '" + name + "', '" + str( age ) + "', '" + nation + "');" )
    cur.execute("SELECT word, frq FROM userword WHERE user_id='" + user_id + "' ;")
    user_words = defaultdict(dict)
    for (word, frq) in cur.fetchall():
        user_words[word] = int(frq)
    cur.close()
    db.close()
    return user_words


def select_words():
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()

    cur.execute("SELECT word_id, word FROM words;")
    wordsID = defaultdict(dict)
    for word_id, word in cur.fetchall():
        wordsID[word] = int(word_id)

    db.commit()
    cur.close()
    db.close()

    return wordsID


def select_words_size():
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    stmt = "select count(*) as cnt from words;"
    cur.execute(stmt)
    cnt = 0
    for ret in cur.fetchall():  # TODO: check if output is correct
        cnt = ret[0]

    db.commit()
    cur.close()
    db.close()

    return cnt


def insert_words_ids(wordsID):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    stmt = "INSERT IGNORE INTO words (word_id, word) VALUES (%s, %s);"

    for word, wid in wordsID.items():
        data = (wid, word)
        cur.execute(stmt, data)

    db.commit()
    cur.close()
    db.close()


def insert_words(words):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    wordsIDs = select_words()
    stmt = "INSERT IGNORE INTO words (word_id, word) VALUES (%s, %s);"

    for word in words:
        if word not in wordsIDs:
            wordsIDs[word] = wordsIDs.__len__()
            data = (wordsIDs[word], word)
            cur.execute(stmt, data)

    db.commit()
    cur.close()
    db.close()


def select_ratings_dic():
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    cur.execute("SELECT user_id, item_id, rating FROM ratings_dict;")
    ratings_dict = {'itemID': list(),
                    'userID': list(),
                    'rating': list()}
    for user_id, item_id, rating in cur.fetchall():
        ratings_dict['rating'].append(float(rating))
        ratings_dict['itemID'].append(int(item_id))
        ratings_dict['userID'].append(user_id)

    db.commit()
    cur.close()
    db.close()

    return ratings_dict


def insert_ratings_dic(ratings_dict):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    stmt = "INSERT INTO ratings_dict (user_id, item_id, rating) VALUES ( %s, %s , %s) ON DUPLICATE KEY UPDATE rating = (%s);"

    for i in range(0, ratings_dict['userID'].__len__()):
        user_id = ratings_dict['userID'][i]
        item_id = ratings_dict['itemID'][i]
        ui_rating = ratings_dict['rating'][i]
        data = (user_id, item_id, ui_rating, ui_rating)
        cur.execute(stmt, data)


def select_interests_ids():
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    cur.execute("SELECT id, interest FROM interests;")
    interest_ids = {}
    for id, interest in cur.fetchall():
        interest_ids[interest] = id

    db.commit()
    cur.close()
    db.close()

    return interest_ids


def insert_interests():
    interests = ["Technology", "Space", "Music", "Sports", "Nature and Animals",
                 "Science", "Fashion", "Programming", "Education", "Movies"]

    iid = select_words_size()
    interestsID = {}
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    stmt = "insert into interests (id, interest) values (%s, %s)"

    for interest in interests:
        data = (iid, interest)
        interestsID[interest] = iid
        cur.execute(stmt, data)
        iid += 1

    db.commit()
    cur.close()
    db.close()

    insert_words_ids(interestsID)


def insert_user_interest(user_id, interests):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()

    interest_ids = select_interests_ids()

    stmt = "INSERT INTO user_interests (user_id, interest_id) VALUES (%s, %s);"

    for i in interests:
        print(user_id,  interest_ids[i], "!!!!!")
        data = (user_id, interest_ids[i])
        cur.execute(stmt, data)

    db.commit()
    cur.close()
    db.close()


def select_user_interest(user_id):
    db = mysql.connector.connect(user='root', password='root', host='localhost', database='search-worm')
    cur = db.cursor()
    stmt = "select interest from interests " \
           "left join user_interests on id = interest_id " \
           "where user_id = %s;"
    data = (user_id)
    cur.execute(stmt, data)
    user_interests = []
    for interest in cur.fetchall():
        user_interests.append(interest)

    db.commit()
    cur.close()
    db.close()

    return user_interests


