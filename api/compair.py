import numpy as np
import pandas as pd
from utils.mongo import Mongo
import time
import threading

# with open("/Ezshop/IDAS/components/features2.pkl", "rb") as f:
#     allVectors = pickle.load(f)
##############################################################################
# with open("/home/ezshop/components/features.pkl", "rb") as f:
#     allVectors1 = pickle.load(f)
# with open("/home/ezshop/components/features1.pkl", "rb") as f:
#     allVectors2 = pickle.load(f)
##############################################################################
# with open("components/features.pkl", "rb") as f:
#     allVectors1 = pickle.load(f)
# with open("components/features1.pkl", "rb") as f:
#     allVectors2 = pickle.load(f)
# allVectors = {**allVectors1, **allVectors2}


vectors = {}


class FeatureModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'features'
    _db_name = 'data_pipline'


features_model = FeatureModel()


def maximum(vecs: dict):
    if vecs == {}:
        mx = 0
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
        time.sleep(86400)


# makes our logic non blocking

thread = threading.Thread(target=schedule)
thread.start()


# class Compair:
#     def __init__(self):
#         pass

def similar_postid(vec, k=5):
    # a = []

    # getting the timestamp
    # dt = datetime.now()

    ####transformationForCNNInput = transforms.Compose([transforms.Resize((224, 224))])
    ####I = Image.open(file)

    # ts1 = datetime.now()
    # a.append(str(ts1 - dt))

    ####newI = transformationForCNNInput(I)
    # ts2 = datetime.now()
    # a.append(str(ts2 - ts1))
    ####vec = img2vec.get_vec(newI)
    # ts3 = datetime.now()
    # a.append(str(ts3 - ts2))
    # vec = np.array(vec)
    sim = np.inner(vec.T, v.T) / (
            (np.linalg.norm(vec, axis=0).reshape(-1, 1)) *
            (np.linalg.norm(v, axis=0).reshape(-1, 1)).T)
    # ts4 = datetime.now()
    # a.append(str(ts4 - ts3))
    # matrix = pd.DataFrame(sim, columns=keys).T
    # ts5 = datetime.now()
    # a.append(str(ts5 - ts4))
    # ts6 = datetime.now()
    # a.append(str(ts6 - ts5))
    return list(pd.DataFrame(sim, columns=keys).T.sort_values(by=0, ascending=False).head(k).index)
