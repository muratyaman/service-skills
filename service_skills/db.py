from pymongo import MongoClient
from bson import ObjectId

from .config import Config


# avoid json serialization issues
def object_id_to_str(row):
    new_row = {}
    for p in row:
        val = row[p]
        if isinstance(val, ObjectId):
            new_row[p] = str(val)  # convert to string
        #elif isinstance(val, object):
        #    new_row[p] = object_id_to_str(val)
        else:
            new_row[p] = val  # copy properties
    return new_row


def get_rows(cursor):
    rows = []
    for row in cursor:
        rows.append(object_id_to_str(row))
    return rows


class Db:

    def __init__(self, adapter):
        self.adapter = adapter
        pass

    def profiles(self):
        return self.adapter.profiles

    def profiles_search(self, params={}, limit_rows=100):
        cursor = self.profiles().find(filter=params, limit=limit_rows)
        return get_rows(cursor)

    def profiles_create(self, data):
        result = self.profiles().insert_one(data)
        return result.inserted_id

    def profiles_retrieve(self, user_id):
        params = {'user_id': user_id}
        row = None
        #rows = self.profiles_search(params, 1)
        #if 0 in rows:
        #    row = object_id_to_str(rows[0])
        row = self.profiles().find_one(params)
        return row

    def profiles_update(self, user_id, skills=[]):
        condition = {'user_id': user_id}
        action = {'$set': {'skills': skills}}
        result = self.profiles().update_one(condition, action)
        return 1 == result.modified_count

    def profiles_delete(self, user_id):
        condition = {'user_id': user_id}
        result = self.profiles().delete_one(condition)
        return 1 == result.deleted_count

    def profiles_upsert(self, user_id, skills):
        condition = {'user_id': user_id}
        replacement = {'user_id': user_id, 'skills': skills}
        upsert = True
        result = self.profiles().replace_one(condition, replacement, upsert)
        return result.upserted_id

    def definitions(self):
        return self.adapter.definitions

    def definitions_search(self, params):
        cursor = self.definitions().find(params)
        return get_rows(cursor)


def get_db(config: Config):
    db_dsn = config.db_dsn
    client = MongoClient(db_dsn)
    db_adapter = client[config.db_name]
    db = Db(db_adapter)
    return db
