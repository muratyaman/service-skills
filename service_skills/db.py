from pymongo import MongoClient
from service_skills.config import Config


class Db:

    def __init__(self, adapter):
        self.adapter = adapter
        pass

    def profiles(self):
        return self.adapter.profiles

    def profiles_search(self, params={}, limit=100):
        return self.profiles().find(params)

    def profiles_create(self, params):
        return self.profiles().insertOne(params)

    def profiles_retrieve(self, user_id):
        condition = {'user_id': user_id}
        return self.profiles().findOne(condition, 1)

    def profiles_update(self, user_id, params):
        condition = {'user_id': user_id}
        action = {'$set':params}
        options = {'upsert':True}
        return self.profiles().updateOne(condition, action, options)

    def profiles_delete(self, user_id):
        condition = {'user_id': user_id}
        return self.profiles().deleteOne(condition)

    def definitions(self):
        return self.adapter.definitions

    def definitions_search(self, params):
        return self.definitions().find(params)


def get_db(config: Config):
    db_dsn = config.db_dsn
    client = MongoClient(db_dsn)
    db_adapter = client[config.db_name]
    db = Db(db_adapter)
    return db
