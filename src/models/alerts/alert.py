import uuid
import datetime
import requests
import src.models.alerts.constants as AlertConstants
from src.models.items.item import Item


class Alert(object):

    def __init__(self, user_email, price_limit, item_id, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    # string representation
    def __repr__(self):
        return "<Alert for {} on item {} with price {}"\
            .format(self.user_email, self.item.name, self.price_limit)

    # sending email alert from mailgun
    @property
    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=('api', AlertConstants.API_KEY),
            data={
                'from': AlertConstants.FROM,
                'to': self.user_email,
                'subject': 'Price limit reached for {}'.format(self.item.name),
                'text': 'We have found a deal (link here)'
            }
        )

    # create a method to check if there are updates to be executed in db
    # each alert will be checked out every 10 minutes as in alert.constants.py
    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, query={
            'last_checked': {'$gte': last_updated_limit}
        })]

    # save to db
    def save_to_mongo(self):
        Database.insert(AlertConstants.COLLECTION, self.json())


    def json(self):
        return {
            '_id': self._id,
            'price_limit': self.price_limit,
            'last_checked': self.last_checked,
            'user_email': self.user_email,
            'item_id': self.item._id
        }