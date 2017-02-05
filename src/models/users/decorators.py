from functools import wraps
from flask import redirect, session, url_for, request

# version 1
from src.app import app

# version 2
# import src.app

# first decorator to be used in models/alerts/views.py -- create_alert
def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            # next=request.path --when the user is logging in will be redirect to this page
            return redirect( url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)
    return decorated_function


# second decorator to be used models/stores/views.py -- for managing stores
def requires_admin_permissions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        # version 1
        if session['email'] not in app.config.ADMINS:
        # version 2
        #if session['email'] not in src.app.app.ADMINS:
            return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)
    return decorated_function


