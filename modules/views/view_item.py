from modules.setup.app import app, session
from modules.setup.database import Item
from modules import helpers
from flask import render_template


@app.route('/category/<int:category_id>/item/<int:item_id>/')
@helpers.category_exists
@helpers.item_exists
def viewItem(item_id, category_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('viewitem.html', item=item)
