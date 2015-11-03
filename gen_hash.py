#!.venv/bin/python3

import bcrypt
import sys

print('Enter token:')
passw = sys.stdin.readline().strip().encode('utf-8')
hash = bcrypt.hashpw(passw, bcrypt.gensalt())
print("slack_token = %s" % str(hash, 'ascii'))
