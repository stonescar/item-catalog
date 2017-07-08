from modules.setup.app import app
from modules import helpers
from flask import render_template


@app.route('/category/<int:category_id>/item/<int:item_id>/')
@helpers.category_exists
@helpers.item_exists
def viewItem(category_id, category, item_id, item):
    return render_template('viewitem.html', item=item)
