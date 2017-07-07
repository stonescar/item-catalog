from modules.setup.app import app, session
from modules.setup.database import Category, Item
from modules import helpers
from flask import render_template


@app.route('/category/<int:category_id>/')
@helpers.category_exists
def viewCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category=category).all()
    return render_template('viewcategory.html', category=category, items=items)
