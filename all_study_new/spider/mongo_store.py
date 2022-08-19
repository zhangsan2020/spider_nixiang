import pymongo


class MongoStore():

    def __init__(self):
        self.mongo_cli = pymongo.MongoClient(host='127.0.0.1', port= 27017)
        self.db = self.mongo_cli['Food_store']

    def insert(self,item):

        result = self.db.food.insert_one(item)
        print(result)