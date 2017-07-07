from modules.setup.app import app
from modules import helpers
from flask import render_template, session as login_session


@app.route('/login/')
def login():
    state = helpers.generateState()
    login_session['state'] = state
    return render_template('login.html', STATE=state)
