from modules.setup.app import app
from modules import helpers
from flask import render_template


@app.route('/category/<int:category_id>/item/<int:item_id>/')
@helpers.category_exists
@helpers.item_exists
def viewItem(item_id, category_id, category, item):
    return render_template('viewitem.html', item=item)
