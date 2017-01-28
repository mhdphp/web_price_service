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