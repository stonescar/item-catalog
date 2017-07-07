from modules.setup.app import app
from modules import helpers
from flask import request, make_response, flash, session as login_session
import json
import httplib2
import os
import sys

ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
client_secret_path = os.path.join(
    ROOT_DIR, 'client_secrets/fb_client_secrets.json')


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(
            'Invalid state parameter'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange client token for long-lived server-side token
    app_id = json.loads(open(
        client_secret_path, 'r').read())['web']['app_id']
    app_secret = json.loads(open(
        client_secret_path, 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    # Strip expire tag from access token
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['access_token'] = token

    # Get user picture
    url = "https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200" % token  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # Create user, if it doesn't already exist
    user_id = helpers.getUserID(login_session['email'])
    if not user_id:
        user_id = helpers.createUser(login_session)
    login_session['user_id'] = user_id

    flash('You are now logged in as %s (%s)' % (
        login_session['username'], login_session['email']))
    return 'success'
