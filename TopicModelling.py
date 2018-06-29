
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

import gensim
from gensim import corpora

import re


def clean(doc):

    doc = re.sub( "[^a-zA-Z\s\\n]", " ", doc )
    doc = re.sub( "\\s+", " ", doc )
    doc = re.sub( '([A-Z]{1})', r'_\1', doc ).lower()

    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def LDA( doc_complete ):

    topic_words = []

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

        topic_words.append(topn_words)
        # if n==1 :
        #     topic_words1.append(topn_words)
        # elif n==2 :
        #     topic_words2.append(topn_words)
        # elif n == 3:
        #     topic_words3.append(topn_words)
        # elif n == 4:
        #     topic_words4.append(topn_words)

    return topic_words