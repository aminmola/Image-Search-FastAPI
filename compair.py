import numpy as np
import pandas as pd
from utils.mongo import Mongo
import time
import threading
from sklearn.neighbors import NearestNeighbors

vectors = {}
knn = NearestNeighbors(n_neighbors=50, metric="cosine")


class FeatureModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'features'
    _db_name = 'data_pipline'


features_model = FeatureModel()


def maximum(vecs: dict):
    if vecs == {}:
        mx = 8000000
    else:
        mx = max(vecs.keys())
    return mx


def task():
    m = maximum(vectors)
    query = {"PostId": {'$gt': m}}
    feature_docs = features_model.collection.find(query)
    for vec in feature_docs:
        vectors[vec['PostId']] = np.array(vec['Feature'], dtype=np.float32)
    global v
    v = np.array(list(vectors.values())).T
    global knn
    knn.fit(v.T)
    global keys
    keys = list(vectors.keys())


def schedule():
    while 1:
        task()
        time.sleep(7200)


thread = threading.Thread(target=schedule)
thread.start()


def similar_postid(vec, k=5):
    return [keys[i] for i in knn.kneighbors(np.expand_dims(vec, 0))[1][0][:k]]


def similar_postid_exact(vec, k=50):
    a = knn.kneighbors(np.expand_dims(vec, 0))
    exact_similar_postid = []
    for m in range(k):
        if a[0][0][m] < 0.01:
            exact_similar_postid.append(keys[a[1][0][m]])
        else:
            break
    return {"exact_similar_postid": exact_similar_postid,
            "rest_of_similar_postid": [keys[i] for i in knn.kneighbors(np.expand_dims(vec, 0))[1][0][m:k]]
            }
