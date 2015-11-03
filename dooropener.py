#!.venv/bin/python3

from datetime import datetime
from flask import (
   Flask,
   render_template,
   Response,
   request,
   send_from_directory,
)
import html
import json
import requests
import configparser

app = Flask(__name__)

def do_open_door():
    print('opened the door')

def log_door(username):
    text = "User *%s* just opened the CWS door via _/dooropen_" % username
    payload = dict(
        text=text,
        username='cwsdoor',
        icon_emoji=':cws:'
    )
    requests.post(slack_webhook, data=json.dumps(payload))

@app.route('/dooropen/', methods=['POST', 'GET'])
def dooropen():
    """
    Standard endpoint
    """
    password = request.args.get('token', '').strip()
    user_id = request.args.get('user_id', '').strip()
    user_name = request.args.get('user_name', '').strip()

    if not bcrypt.hashpw(password, slack_token) == slack_token:
        return 'Invalid token'

    log_door('%s (%s)' % (user_name, user_id))
    do_open_door()

    return 'Door is open'

config = configparser.ConfigParser()
config.read('config.txt')
slack_token = config['dooropener']['slack_token']
slack_webhook = config['dooropener']['slack_webhook'].strip('\'"')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
