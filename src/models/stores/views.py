from flask import Blueprint, render_template
from src.models.stores.store import Store


# define stores blueprint
store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/stores_index.jinja2', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return 'This is the store page'


@store_blueprint.route('/new', methods=['GET', 'POST'])
def create_store():
    return 'This is the new store creation page'

