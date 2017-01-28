from flask import Blueprint


# define the user_blueprint
user_blueprint = Blueprint('users', __name__)


# define login end-point
@user_blueprint.route('/login')
def login_user():
    pass


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