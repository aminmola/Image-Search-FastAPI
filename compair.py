import numpy as np
from utils.mongo import Mongo
import time
import threading
from sklearn.neighbors import NearestNeighbors


class FeatureModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'features'
    _db_name = 'data_pipline'


features_model = FeatureModel()


# def maximum(vecs: dict):
#     if vecs == {}:
#         mx = 10680000
#     else:
#         mx = max(vecs.keys())
#     return mx


class FindSimilar():
    def __init__(self, ):
        self.keys = []
        self.knn = NearestNeighbors(n_neighbors=50, metric="cosine")
        self.thread = threading.Thread(target=self.schedule)
        self.thread.start()
        self.vectors = {}

    def schedule(self):
        while 1:
            self.update()
            time.sleep(72000)

    def update(self):
        if self.keys:
            max_postId = max(self.keys)
        else:
            max_postId = 9000000
        # m = maximum(vectors)
        query = {"PostId": {'$gt': max_postId}}
        feature_docs = features_model.collection.find(query)
        for vec in feature_docs:
            self.vectors[vec['PostId']] = np.array(vec['Feature'], dtype=np.float32)
        v = np.array(list(self.vectors.values())).T
        self.knn.fit(v.T)
        self.keys = list(self.vectors.keys())

    def similar_postid(self, vec, k=5):
        return [self.keys[i] for i in self.knn.kneighbors(np.expand_dims(vec, 0))[1][0][:k]]

    def similar_postid_exact(self, vec, k=50):
        a = self.knn.kneighbors(np.expand_dims(vec, 0))
        exact_similar_postid = []
        for m in range(k):
            if a[0][0][m] < 0.01:
                exact_similar_postid.append(self.keys[a[1][0][m]])
            else:
                break
        return {"exact_similar_postid": exact_similar_postid,
                "rest_of_similar_postid": [self.keys[i] for i in self.knn.kneighbors(np.expand_dims(vec, 0))[1][0][m:k]]
                }
