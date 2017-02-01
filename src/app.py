from flask import Flask
from flask import render_template
from src.common.database import Database

app = Flask(__name__)
# load config file
app.config.from_object('config')
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


# register the blueprints
from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
from src.models.users.views import user_blueprint
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
app.register_blueprint(store_blueprint, url_prefix='/stores')
app.register_blueprint(user_blueprint, url_prefix='/users')


