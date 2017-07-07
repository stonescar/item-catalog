from modules.setup.app import app, session
from modules.setup.database import Category, Item
from flask import jsonify


@app.route('/items/JSON/')
def allItemsJSON():
    categories = session.query(Category).all()
    catsSerialized = []
    for c in categories:
        items = session.query(Item).filter_by(category_id=c.id).all()
        catsSerialized.append(c.serialize(items))
    return jsonify(Categories=catsSerialized)
