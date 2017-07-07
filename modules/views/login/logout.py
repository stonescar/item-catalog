from modules.setup.app import app
from modules.views.login import facebook, google, github
from flask import redirect, url_for, flash, session as login_session


@app.route('/logout/')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            facebook.fbdisconnect()
            del login_session['facebook_id']
        if login_session['provider'] == 'google':
            google.gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'github':
            github.ghdisconnect()
        del login_session['provider']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        flash('You have successfully been logged out')
    else:
        flash('!E!You weren\'t logged in to begin with')
    return redirect(url_for('front'))
