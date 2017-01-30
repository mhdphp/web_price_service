import uuid
import re
from src.common.database import Database
import src.models.stores.constants as StoreItems
import src.models.stores.errors as StoreErrors


class Store(object):

    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    # string representation
    def __repr__(self):
        return "<Store {}>".format(self.name)


    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }


    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(collection=StoreItems.COLLECTION, query={'_id': id}))


    def save_to_mongo(self):
        Database.insert(collection=StoreItems.COLLECTION, data=self.json())


    @classmethod
    def get_by_name(cls, name):
        return cls(**Database.find_one(collection=StoreItems.COLLECTION, query={'name': name}))


    # return object of a store when a url_prefix is given
    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(StoreItems.COLLECTION, \
                                       query={'url_prefix': {"$regex": '^{}'.format(url_prefix)}}))


    # find a store by URL
    @classmethod
    def find_by_url(cls, url):
        """
        Return a store from url like : "http://www.johnlewis.com/item/akdowdkaewe.html"
        :param url: the item's URL
        :return: a Store, or raise StoreNotFoundException if no store matches the URL
        """
        for i in range(0, len(url)+1):
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                raise StoreErrors.StoreNotFoundException('No store found with this url.')


    # second way to find a store from database given a extended url name
    @classmethod
    def find_store_from_url(cls, url):
        url_regex = re.compile(r'http(s)*:\/\/\w+\.\w+\.?\w+\/')
        mo = url_regex.search(url)
        str_val = str(mo.group())
        url_prefix = str_val[:len(str_val)-1]

        return cls(**Database.find_one(StoreItems.COLLECTION, {'url_prefix': url_prefix}))