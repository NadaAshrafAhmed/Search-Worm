import mysql.connector



def add_user(id,name,age,nation):
    db = mysql.connector.connect( user='nada', password='root', host='localhost', database='search-worm' )
    cur = db.cursor()
    cur.execute( "INSERT INTO user VALUES ('"+id+"', '"+name+"', '"+str(age)+"', '"+nation+"');" )
    cur.execute( "SELECT * FROM user" )
    for r in cur.fetchall():
        print( r )
    db.commit()

    cur.close()
    db.close()
def user_exist(id):
    db = mysql.connector.connect( user='nada', password='root', host='localhost', database='search-worm' )
    cur = db.cursor()
    cur.execute( "SELECT name FROM user WHERE id='"+id+"';" )
    cur.fetchall()
    return (cur.rowcount>0)

def add_word(user_id, words):
    db = mysql.connector.connect( user='nada', password='root', host='localhost', database='search-worm' )
    cur = db.cursor()
    # cur.execute( "INSERT INTO user VALUES ('" + id + "', '" + name + "', '" + str( age ) + "', '" + nation + "');" )
    cur.execute( "SELECT word, frq FROM userword WHERE user_id='"+user_id+"' ;" )
    user_words={}
    for (word, frq) in cur.fetchall():
        user_words[word]=frq
    new_words=[]
    updated_words=[]
    for word in words:
        if word in user_words:
            user_words[word]+=1
            updated_words.append(word)
        else:
            user_words[word]=1
            new_words.append(word)

    new_words = list(set(new_words))
    updated_words = list(set(updated_words))

    for word in new_words:
        cur.execute( "INSERT INTO words VALUES ('" + word + "');" )
        cur.execute( "INSERT INTO userword VALUES ('" + user_id + "', '"+word+"', '1');" )
    for word in updated_words:
        cur.execute( "UPDATE userword SET frq='" + str(user_words[word]) + "' WHERE user_id= '"+user_id+"' and word= '"+word+"';" )


    db.commit()

    cur.close()
    db.close()

def add_topic(w1, w2, w3):
    db = mysql.connector.connect( user='nada', password='root', host='localhost', database='search-worm' )
    cur = db.cursor()
    cur.execute( "SELECT max(id) as mx FROM topic ;" )
    id=0;
    for mx in cur.fetchall():
        id=mx[0]
    if(id):
        id+=1;
    else:
        id=1
    cur.execute( "INSERT INTO topic VALUES ('" + w3 + "', '" + w1 + "', '"+w2+"', '"+str(id)+"');" )

    db.commit()

    cur.close()
    db.close()


# # you must create a Cursor object. It will let
# #  you execute all the queries you need
# cur = db.cursor()
#
# # Use all the SQL you like
# cur.execute("SELECT * FROM words")
#
# # print all the first cell of all the rows
# for row in cur.fetchall():
#     print (row[0])
#
# db.close()