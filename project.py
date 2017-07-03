#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database_setup import Base, Category, Item
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from flask import (Flask, render_template, request,
                   redirect, url_for, flash, jsonify)
from modules import get_image, helpers


app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.context_processor
def utility_processor():
    def get_categories():
        categories = session.query(Category).order_by(Category.name).all()
        for c in categories:
            c.count = session.query(Item).filter_by(category_id=c.id).count()
        return categories
    return dict(get_categories=get_categories)


@app.route('/')
def front():
    recent = session.query(Item).order_by(desc(Item.time)).limit(10).all()
    return render_template('front.html', recent=recent)


@app.route('/category/<int:category_id>/')
@helpers.category_exists
def viewCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category=category).all()
    return render_template('viewcategory.html', category=category, items=items)


@app.route('/category/edit/')
def editCategories():
    categories = session.query(Category).order_by(Category.name).all()
    return render_template('editcategories.html', categories=categories)


@app.route('/category/new/', methods=['POST', 'GET'])
def newCategory():
    if request.method == 'POST':
        category = Category(name=request.form['name'])
        session.add(category)
        session.commit()
        flash('Category <b>%s</b> added' % category.name)
        return redirect(url_for('viewCategory', category_id=category.id))
    return render_template('newcategory.html')


@app.route('/category/<int:category_id>/edit/', methods=['POST', 'GET'])
@helpers.category_exists
def editCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        category.name = request.form['name']
        session.add(category)
        session.commit()
        flash('Category <b>%s</b> has been edited' % category.name)
        return redirect(url_for('editCategories'))
    else:
        return render_template('editcategory.html', category=category)


@app.route('/category/<int:category_id>/clear/', methods=['POST', 'GET'])
@helpers.category_exists
def clearCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        items = session.query(Item).filter_by(category=category).all()
        for item in items:
            session.delete(item)
        session.commit()
        flash('All items in category <b>%s</b> has been deleted' %
              category.name)
        return redirect(url_for('editCategories'))
    else:
        return render_template('clearcategory.html', category=category)


@app.route('/category/<int:category_id>/delete/', methods=['POST', 'GET'])
@helpers.category_exists
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        items = session.query(Item).filter_by(category=category).all()
        for item in items:
            session.delete(item)
        session.delete(category)
        session.commit()
        flash('Category <b>%s</b> has been deleted' % category.name)
        return redirect(url_for('editCategories'))
    else:
        return render_template('deletecategory.html', category=category)


@app.route('/category/<int:category_id>/item/<int:item_id>/')
@helpers.category_exists
@helpers.item_exists
def viewItem(item_id, category_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('viewitem.html', item=item)


@app.route('/item/new/', methods=['POST', 'GET'])
def newItem():
    if request.method == 'POST':
        name = request.form['name']
        if request.form['random-img']:
            picture = get_image.randomImage(name)
        else:
            picture = request.form['picture'].encode("utf-8")
        item = Item(name=name,
                    description=request.form['description'],
                    picture=picture,
                    category_id=request.form['category'])
        session.add(item)
        session.commit()
        flash('Item <b>%s</b> added' % item.name)
        return redirect(url_for('viewCategory',
                                category_id=item.category_id))
    else:
        if request.referrer and 'category' in request.referrer:
            referrer = int(request.referrer.split("/")[4])
            return render_template('newitem.html', ref=referrer)
        else:
            return render_template('newitem.html')


@app.route('/category/<int:category_id>/item/<int:item_id>/edit/',
           methods=['POST', 'GET'])
@helpers.category_exists
@helpers.item_exists
def editItem(item_id, category_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        if request.form['random-img']:
            item.picture = get_image.randomImage(item.name)
        else:
            item.picture = request.form['picture']
        item.category_id = request.form['category']
        session.add(item)
        session.commit()
        flash('Item <b>%s</b> has been edited' % item.name)
        return redirect(url_for('viewItem',
                                category_id=category_id,
                                item_id=item_id))
    else:
        categories = session.query(Category).all()
        return render_template('edititem.html',
                               item=item,
                               categories=categories)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete/',
           methods=['POST', 'GET'])
@helpers.category_exists
@helpers.item_exists
def deleteItem(item_id, category_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item <b>%s</b> has been deleted' % item.name)
        return redirect(url_for('viewCategory', category_id=item.category_id))
    else:
        return render_template('deleteitem.html', item=item)


@app.route('/items/JSON/')
def allItemsJSON():
    categories = session.query(Category).all()
    catsSerialized = []
    for c in categories:
        items = session.query(Item).filter_by(category_id=c.id).all()
        catsSerialized.append(c.serialize(items))
    return jsonify(Categories=catsSerialized)


@app.route('/category/<int:category_id>/JSON/')
@helpers.category_exists
def categoryJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/login/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
