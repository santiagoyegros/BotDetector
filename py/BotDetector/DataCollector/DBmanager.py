'''
@author: Santirrium
'''
from collections import defaultdict
from pymongo import MongoClient

host = 'localhost'
port = '27017'
db_name = 'BotDetector'

class DBmanager:
    __db = None
    __host = None
    __collection = ''
    
    def __init__(self, collection):
        self.__host = host
        self.__port = port
        client = MongoClient(self.__host+':'+self.__port)
        self.__db = client[db_name]
        self.__collection = collection
        
    def num_records_collection(self):
        return self.__db[self.__collection].find({}).count()

    def clear_collection(self):
        self.__db[self.__collection].remove({})

    def save_record(self, record_to_save):
        self.__db[self.__collection].insert(record_to_save)

    def find_record(self, query):
        return self.__db[self.__collection].find_one(query)

    def update_record(self, filter_query, new_values, create_if_doesnt_exist=False):
        return self.__db[self.__collection].update_one(filter_query, {'$set': new_values},
                                                       upsert=create_if_doesnt_exist)

    def remove_field(self, filter_query, old_values, create_if_doesnt_exist=False):
        return self.__db[self.__collection].update_one(filter_query, {'$unset': old_values},
                                                       upsert=create_if_doesnt_exist)

    def search(self, query):
        return self.__db[self.__collection].find(query)

    def search_one(self, query, i):
        return self.__db[self.__collection].find(query)[i]

    def remove_record(self, query):
        self.__db[self.__collection].delete_one(query)
        
    def aggregate(self, pipeline):
        return [doc for doc in self.__db[self.__collection].aggregate(pipeline, allowDiskUse=True)]


