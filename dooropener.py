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
    os.system('sudo rpio --setoutput 18:1; sudo rpio --setoutput 18:0')
    print('opened the door')

def log_message(msg):
    payload = dict(
        text=msg,
        username='cwsdoor',
        icon_emoji=':cws:'
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

    if not bcrypt.hashpw(password, slack_token) == slack_token:
        return 'Invalid token'

    msg = "User *%s (%s)* just opened the CWS door via _/dooropen_" % \
        (user_name, user_id)
    log_message(msg)

    do_open_door()

    return 'Door is open'

config = configparser.ConfigParser()
config.read('config.txt')
slack_token = config['dooropener']['slack_token'].encode('utf-8')
slack_webhook = config['dooropener']['slack_webhook'].strip('\'"')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050)
