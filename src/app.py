from flask import Flask, render_template
from src.common.database import Database

# version 2
# import src.models.alerts.views
# import src.models.stores.views
# import src.models.users.views


app = Flask(__name__)
# load config file
app.config.from_object('src.config')
# create a secure key for cookies generate by Flask to be secure
app.secret_key = "123"


@app.route('/rahan')
def rahan():
    return "This is rahan"


#initialize database
@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template('home.jinja2')

# version 1
# register the blueprints - initial solution
from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
from src.models.users.views import user_blueprint
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
app.register_blueprint(store_blueprint, url_prefix='/stores')
app.register_blueprint(user_blueprint, url_prefix='/users')


# version 2
# app.register_blueprint(src.models.users.views.user_blueprint, url_prefix='/users')
# app.register_blueprint(src.models.alerts.views.alert_blueprint, url_prefix='/alerts')
# app.register_blueprint(src.models.stores.views.store_blueprint, url_prefix='/stores')


