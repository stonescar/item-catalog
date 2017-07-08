from modules.setup.app import app, session
from modules.setup.database import Item
from modules import helpers
from flask import jsonify


@app.route('/category/<int:category_id>/JSON/')
@helpers.category_exists
def categoryJSON(category_id, category):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Category=category.serialize(items))
