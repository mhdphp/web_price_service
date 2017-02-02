from flask import Blueprint

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
    pass


@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass
