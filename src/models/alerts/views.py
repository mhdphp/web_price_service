from flask import Blueprint, render_template, request, session, redirect, url_for
from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    return 'This is the alerts index'

# create new alert
@alert_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login
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
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    # return redirect(url_for('users.user_alerts'))
    # return to the alerts/alert.jinja2
    return redirect(url_for('.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    # return to the list of user's alerts
    # return redirect(url_for('users.user_alerts'))
    # return to the alerts/alert.jinja2, '.' means that is of this page
    return redirect(url_for('.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/<string:alert_id>')  # /alerts/<string:alert_id>
# @alert_blueprint.route('/alert')
@user_decorators.requires_login
def get_alert_page(alert_id):
    # get the alert object from the db
    alert = Alert.find_by_id(alert_id)
    # passing the alert object in the template view
    return render_template('alerts/alert.jinja2', alert=alert)


@alert_blueprint.route('/check_price/<string:alert_id>')
#@user_decorators.requires_login
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))



