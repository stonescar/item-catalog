from modules.setup.app import app
from modules import helpers
from flask import redirect, request, url_for, flash, session as login_session
import json
import requests
import os
import sys

ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
client_secret_path = os.path.join(
    ROOT_DIR, 'client_secrets/gh_client_secrets.json')


@app.route('/ghconnect', methods=['POST', 'GET'])
def ghconnect():
    if 'code' in request.args:
        url = 'https://github.com/login/oauth/access_token'
        payload = {
            'client_id': json.loads(open(
                client_secret_path, 'r').read())['web']['client_id'],
            'client_secret': json.loads(open(
                client_secret_path, 'r').read())['web']['client_secret'],
            'code': request.args['code'],
            'state': login_session['state']
        }
        headers = {'Accept': 'application/json'}
        r = requests.post(url, params=payload, headers=headers)
        response = r.json()
        if 'access_token' in response:
            login_session['access_token'] = response['access_token']
        else:
            app.logger.error('GitHub didn\'t return an access token')
        url = 'https://api.github.com/user?access_token=%s' % login_session['access_token']  # NOQA
        r = requests.get(url)
        response = r.json()
        login_session['provider'] = 'github'
        login_session['username'] = response['name']
        login_session['picture'] = response['avatar_url']
        # Get user's email
        url = 'https://api.github.com/user/emails?access_token=%s' % login_session['access_token']  # NOQA
        r = requests.get(url)
        response = r.json()
        login_session['email'] = response[0]['email']
        # Create user, it it doesn't already exist
        user_id = helpers.getUserID(login_session['email'])
        if not user_id:
            user_id = helpers.createUser(login_session)
        login_session['user_id'] = user_id
        flash('You are now logged in as %s (%s)' % (
            login_session['username'], login_session['email']))
        return redirect(url_for('front'))
    return '', 404
