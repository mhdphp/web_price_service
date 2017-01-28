from flask import Flask
from src.common.database import Database

app = Flask(__name__)
# load config file
app.config.from_object('config')


#initialize database
@app.before_first_request
def init_db():
    Database.initialize()


# register the user_blueprint
from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')