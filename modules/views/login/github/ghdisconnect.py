from flask import session as login_session
import json
import httplib2
import os
import sys

ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
client_secret_path = os.path.join(
    ROOT_DIR, 'client_secrets/gh_client_secrets.json')


def ghdisconnect():
    client_id = json.loads(open(
        client_secret_path, 'r').read())['web']['client_id']
    url = 'https://api.github.com/applications/%s/tokens/%s' % (client_id, login_session['access_token'])  # NOQA
    h = httplib2.Http()
    h.request(url, 'DELETE')[1]
