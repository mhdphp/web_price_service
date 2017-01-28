from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect

from src.models.users.user import User

# define the user_blueprint
user_blueprint = Blueprint('users', __name__)


# define login end-point
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['hashed']

        # check if the email, password are valid
        if User.is_login_valid(email, password):
            session['email'] = email
            # go to the def user_alerts()
            return redirect(url_for(".user_alerts"))
    return render_template("users/login.html")


# define logout end-point
@user_blueprint.route('/logout')
def logout_user():
    pass


# define register end-point
@user_blueprint.route('/register')
def register_user():
    pass


# define alerts end-point
@user_blueprint.route('/alerts')
def user_alerts():
    pass


# check-up alerts for a specified user
@user_blueprint.route('/check_alerts/string:user_id')
def check_user_alerts(user_id):
    pass