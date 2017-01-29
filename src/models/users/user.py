import uuid

from src.common.database import Database
from src.common.utils import Utils
# import both classes from src.models.users.errors and give a name UserErrors
import src.models.users.errors as UserErrors


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    # string representation
    def __repr__(self):
        return "<User {}".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies in the database if the email, password pair is valid or note.
        Check if email exists, and if the password associated with the email is valid.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        # password in sha512 -> pbkdf2_sha512
        user_data = Database.find_one(collection='users', query={"email": email})

        if user_data is None:
            # tell the user that he email provided is not found in the database
            raise UserErrors.UserNotExistsError('Your user does not exist.')

        if not Utils.checked_hashed_password(password, user_data['password']):
            # tell the user that the password provided is wrong
            raise UserErrors.IncorrectPasswordError('The password provided was wrong.')

        return True


    @staticmethod
    def register_user(email, password):
        """
        This method registers an user with email and password
        The password already comes sha512
        :param email: user's email -- to be check is not already in the database
        :param password: sha512 hashed password to be converted into pbkdf2-sha512
        :return: True if user is registered, and False otherwise
        """

        # check the db for the email provided
        user_data = Database.find_one(collection='users', query={'email': email})

        # if we got a not None result
        if user_data is not None:
            # tell the user that he email provided is already in the db
            raise UserErrors.UserAlreadyRegisteredError('The email provided already exists.')

        if not Utils.email_is_valid(email):
            # tell the suer that the email is not formatted as an email
            raise UserErrors.InvalidEmailError('The email has not a proper format.')

        # if everything is OK, save the new user to the db
        User(email, Utils.hash_password(password)).save_to_db()

        return True


    def save_to_db(self):
        Database.insert(collection='users', data=self.json())


    def json(self):
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
