import os

ALERT_TIMEOUT = 10
COLLECTION = "alerts"
URL = os.environ.get('MAILGUN_URL')
API_KEY = os.environ.get('API_KEY')
FROM = os.environ.get('MAILGUN_FROM')
