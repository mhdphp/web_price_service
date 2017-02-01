from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect
import src.models.users.errors as UsersErrors

from src.models.users.user import User

# define the user_blueprint
user_blueprint = Blueprint('users', __name__)


# define login end-point
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['hashed']

        try:
            # check if the email, password are valid
            if User.is_login_valid(email, password):
                session['email'] = email
                # go to the def user_alerts()
                return redirect(url_for(".user_alerts"))
        # except UsersErrors.IncorrectPasswordError as e:
        #     return e.message
        # except UsersErrors.UserNotExistsError as e:
        #     return e.message
        # a shorter line of code
        except UsersErrors.UserError as e:
            return e.message

    return render_template("users/login.jinja2")


# define the register end-point
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_view_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['hashed']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UsersErrors.UserError as e:
            return e.message

    return render_template('users/register.jinja2')


# define logout end-point
@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


# define register end-point
@user_blueprint.route('/register')
def register_user():
    pass


# define alerts end-point
@user_blueprint.route('/alerts')
def user_alerts():
    return "This is the alert page."


# check-up alerts for a specified user
@user_blueprint.route('/check_alerts/string:user_id')
def check_user_alerts(user_id):
    pass