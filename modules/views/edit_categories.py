from modules.setup.app import app, session
from modules.setup.database import Category
from modules import helpers
from flask import render_template


@app.route('/category/edit/')
@helpers.login_required
def editCategories():
    categories = session.query(Category).order_by(Category.name).all()
    return render_template('editcategories.html', categories=categories)
