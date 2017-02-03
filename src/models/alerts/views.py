from flask import Blueprint
from flask import render_template
from flask import request
from flask import session

from src.models.alerts.alert import Alert
from src.models.items.item import Item

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    return 'This is the alerts index'

# create new alert
@alert_blueprint.route('/new', methods=['GET', 'POST'])
def create_alert():
    if request.method == 'POST':
        # get the values of the variables from the form
        name = request.form['name']
        url = request.form['url']
        price_limit = request.form['price_limit']

        # now we must create an item object and save it to the database
        item = Item(name, url)
        item.save_to_mongo()

        # after that we may create the alert object
        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price() # this is already saved alert to the database

    # if is 'GET'
    return render_template('alerts/new_alert.jinja2')


@alert_blueprint.route('/deactivate/<string:alert_id>')
# @alert_blueprint.route('/deactivate')
def deactivate_alert(alert_id):
    pass


@alert_blueprint.route('/<string:alert_id>')  # /alerts/<string:alert_id>
# @alert_blueprint.route('/alert')
def get_alert(alert_id):
    # get the alert object from the db
    alert = Alert.find_by_id(alert_id)
    # passing the alert object in the template view
    return render_template('alerts/alert.jinja2', alert=alert)


@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass
