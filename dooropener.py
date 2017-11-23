#!.venv/bin/python3

from flask import (
   Flask,
   Response,
   request,
)
import bcrypt
import configparser
import json
import os
import requests
from subprocess import Popen, PIPE

app = Flask(__name__)

def do_open_door():
    os.system('sudo rpio --setoutput 18:1; sleep 1s; sudo rpio --setoutput 18:0')
    print('opened the door')

def log_message(msg):
    payload = dict(
        text=msg,
        username='rockethub-door-opener',
        icon_emoji=':door:'
    )
    requests.post(slack_webhook, data=json.dumps(payload))

@app.route('/lan_ip/', methods=['GET'])
def lan_ip():
    """
    Standard endpoint
    """
    ret = Popen(["/sbin/ifconfig", "wlan0"], stdout=PIPE).communicate()[0]
    return Response(ret, mimetype='text/plain')

@app.route('/dooropen/', methods=['POST'])
def dooropen():
    """
    Standard endpoint
    """
    password = request.form['token'].strip().encode('utf-8')
    user_id = request.form['user_id'].strip()
    user_name = request.form['user_name'].strip()

    # Check the provided password against all stored tokens.
    access_allowed = None
    for slack_token in slack_tokens:
        if bcrypt.hashpw(password, slack_token) == slack_token:
            access_allowed = True
            break

    if not access_allowed:
        return 'Invalid token'

    msg = ":office: :door: User *%s (%s)* just opened the RocketHub door via _/dooropen_" % \
        (user_name, user_id)
    log_message(msg)

    do_open_door()

    return 'Door is open'

config = configparser.ConfigParser()
config.read('config.txt')
slack_tokens = [x.encode('utf-8') for x in config['dooropener']['slack_tokens'].split(',')]
slack_webhook = config['dooropener']['slack_webhook'].strip('\'"')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050)
