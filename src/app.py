from flask import Flask

app = Flask(__name__)
# load config file
app.config.from_object('config')

@app.route('/')
def hi_world():
    return 'Hi, world'