from passlib.hash import pbkdf2_sha512

class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: the sha512 from the login/register form
        :return: A sha512 -> pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def checked_hashed_password(password, hashed_password):
        """
        Check that the password that the user sent match the password in the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: shat512-hashed password
        :param hashed_password: pbkdf2-shat512 encrypted password
        :return: True if password matches, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

