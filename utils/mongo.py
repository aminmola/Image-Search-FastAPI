import os
import urllib.parse
from pymongo import MongoClient

import utils.config as cfg


class MongoConnection:
    _instances = {}

    @staticmethod
    def get_instance(connection_name, db_name):
        key = str(os.getpid()) + str(connection_name)
        if key not in MongoConnection._instances:
            MongoConnection._instances[key] = MongoConnection(connection_name, db_name)
        return MongoConnection._instances[key]

    def __init__(self, connection_name, db_name):
        username = cfg.MONGO_USERNAME
        repset = cfg.MONGO_REPSET
        if repset is not None:
            if username is not None:
                password = cfg.MONGO_PASSWORD
                # auth_mechanism = cfg.MONGO_authMechanism
                password = urllib.parse.quote_plus(password)
                username = urllib.parse.quote_plus(username)
                self.connection = MongoClient(
                    'mongodb://%s:%s@' % (username, password) + cfg.MONGO_HOST + '/?replicaSet=' + repset)

            else:
                self.connection = MongoClient(
                    cfg.MONGO_HOST,
                    replicaSet=repset,
                    authSource=db_name, )
        else:
            if username is not None:
                password = cfg.MONGO_PASSWORD
                password = urllib.parse.quote_plus(password)
                username = urllib.parse.quote_plus(username)
                host = cfg.MONGO_HOST
                port = cfg.MONGO_PORT
                self.connection = MongoClient(
                    'mongodb://%s:%s@' % (username, password) + host)

            else:
                self.connection = MongoClient(
                    cfg.MONGO_HOST,
                    authSource=db_name, )


class Mongo:
    _connection_name = ''
    _collection_name = ''
    _db_name = ''
    collection = None

    def __init__(self):
        mongoConnection = MongoConnection.get_instance(self._connection_name, self._db_name)
        self.connection = mongoConnection.connection
        self.collection = self.connection[self._db_name][self._collection_name]

    def update(self, query, data):
        modification = {'$set': data}
        return self.collection.update_many(query, modification)

    def exist(self, query):
        peer = self.collection.count(query)
        return peer > 0

    def delete(self, query):
        return self.collection.delete_many(query)

    def find_one(self, query):
        return self.collection.find_one(query)

    def find(self, query):
        return self.collection.find(query)

    def insert_many(self, data):
        return self.collection.insert_many(data)

    def insert_one(self, data):
        return self.collection.insert_one(data)

    def insert_ignore_duplicate(self, data):
        try:
            return self.collection.insert_many(data, ordered=False)
        except:
            pass

    def update_upsert(self, query, data):
        self.collection.update_many(query, data, upsert=True)

    def bulk_execute(self, bulk):
        return self.collection.bulk_write(bulk)
