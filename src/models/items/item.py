import uuid
import requests
from bs4 import BeautifulSoup
import re
from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        tag_name = store.tag_name
        # is the html expression from inspect element in soup.find()
        query = store.query
        self.price = self.load_price(tag_name, query)
        self._id = uuid.uuid4().hex if _id is None else _id

    # string representation
    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    # load item
    def load_price(self, tag_name, query):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, 'html.parser')
        # soup.find(tag_name, query) -- query is a dictionary
        # element = soup.find("span", {"itemprop":"price", "class":"now-price"})
        element = soup.find(tag_name, query)
        string_price = element.text.strip()

        # isolate the price as a floating number using the regular expressions
        pattern = re.compile('(\d+\.\d+)')  # $240.99 -> 240.99
        match = pattern.search(string_price)
        # return the price: 240.99
        return match.group()

    def save_to_mongo(self):
        Database.insert(ItemConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url
        }
