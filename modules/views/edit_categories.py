from modules.setup.app import app, session
from modules.setup.database import Category
from flask import (render_template, redirect, flash,
                   url_for, session as login_session)


@app.route('/category/edit/')
def editCategories():
    # Require login
    if 'username' in login_session:
        categories = session.query(Category).order_by(Category.name).all()
        return render_template('editcategories.html', categories=categories)
    else:
        flash('!E!You must log in first')
        return redirect(url_for('login'))
