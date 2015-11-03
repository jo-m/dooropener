#!.venv/bin/python3

import bcrypt
import sys

print('Enter token:')
passw = sys.stdin.readline()
hash = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
print("slack_token = '%s'" % str(hash, 'ascii'))
