
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans

import pandas as pd
import numpy as np

def k_means(documents):

    clusters = []

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

    return clusters