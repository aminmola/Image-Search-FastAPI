import numpy as np
import pandas as pd
from utils.mongo import Mongo
import time
import threading

vectors = {}


class FeatureModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'features'
    _db_name = 'data_pipline'


features_model = FeatureModel()


def maximum(vecs: dict):
    if vecs == {}:
        mx = 9000000
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
    global keys
    keys = list(vectors.keys())


def schedule():
    while 1:
        task()
        time.sleep(400)


thread = threading.Thread(target=schedule)
thread.start()


def similar_postid(vec, k=5):
    sim = np.inner(vec.T, v.T) / (
            (np.linalg.norm(vec, axis=0).reshape(-1, 1)) *
            (np.linalg.norm(v, axis=0).reshape(-1, 1)).T)
    return list(pd.DataFrame(sim, columns=keys).T.sort_values(by=0, ascending=False).head(k).index)
