from flask import Blueprint
from flask import render_template

from src.models.alerts.alert import Alert

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    return 'This is the alerts index'


@alert_blueprint.route('/new')
def create_alert():
    pass


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
