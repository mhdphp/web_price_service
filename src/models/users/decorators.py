from functools import wraps
from flask import redirect, session, url_for, request

# first decorator to be used in models/alerts/views.py -- create_alert

def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            # next=request.path --when the user is logging in will be redirect to this page
            return redirect( url_for('uses.login_user', next=request.path))
        return func(*args, **kwargs)
    return decorated_function



