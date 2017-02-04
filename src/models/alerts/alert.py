import uuid
import datetime
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item


class Alert(object):

    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active


    # string representation
    def __repr__(self):
        return "<Alert for {} on item {} with price {}"\
            .format(self.user_email, self.item.name, self.price_limit)


    # sending email alert from mailgun
    def send_email(self):
        return requests.post(
            AlertConstants.URL,
            auth=('api', AlertConstants.API_KEY),
            data={
                'from': AlertConstants.FROM,
                'to': self.user_email,
                'subject': 'Price limit reached for {}'.format(self.item.name),
                'text': 'We have found a deal ({})'.format(self.item.url)
            }
        )


    # create a method to check if there are updates to be executed in db
    # each alert will be checked out every 10 minutes as in alert.constants.py
    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, query={
            'last_checked': {'$lte': last_updated_limit},
            # update only the active alerts
            'active': True
                })]


    # save to db
    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {'_id': self._id}, self.json())


    def json(self):
        return {
            '_id': self._id,
            'price_limit': self.price_limit,
            'last_checked': self.last_checked,
            'user_email': self.user_email,
            'item_id': self.item._id,
            'active': self.active
        }


    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price


    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send_email()


    # return list of objects alerts for the specified user
    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'user_email':user_email})]


    # find an alert by an id
    @classmethod
    def find_by_id(cls, alert_id):
        """
        Returns an object with the properties as in database
        :param alert_id:
        :return: an alert object with(user_email, price_limit, item, last_checked, _id)
        """
        return cls(**Database.find_one(collection=AlertConstants.COLLECTION, query={'_id': alert_id}))


    # deactivate method
    def deactivate(self):
        self.active = False
        self.save_to_mongo()


    # activate method
    def activate(self):
        self.active = True
        self.save_to_mongo()


    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id':self._id})