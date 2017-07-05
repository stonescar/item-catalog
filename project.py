#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database_setup import Base, Category, Item
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, session as login_session, make_response)
import json
import httplib2
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
    # Require login
    if 'username' in login_session:
        categories = session.query(Category).order_by(Category.name).all()
        return render_template('editcategories.html', categories=categories)
    else:
        flash('!E!You must log in first')
        return redirect(url_for('login'))


@app.route('/category/new/', methods=['POST', 'GET'])
def newCategory():
    # Require login
    if 'username' in login_session:
        if request.method == 'POST':
            category = Category(name=request.form['name'],
                                user_id=login_session['user_id'])
            session.add(category)
            session.commit()
            flash('Category <b>%s</b> added' % category.name)
            return redirect(url_for('viewCategory', category_id=category.id))
        return render_template('newcategory.html')
    else:
        flash('!E!You must log in first')
        return redirect(url_for('login'))


@app.route('/category/<int:category_id>/edit/', methods=['POST', 'GET'])
@helpers.category_exists
def editCategory(category_id):
    # Require login
    if 'username' in login_session:
        category = session.query(Category).filter_by(id=category_id).one()
        # See if user is category creator
        if login_session['user_id'] == category.user.id:
            if request.method == 'POST':
                category.name = request.form['name']
                session.add(category)
                session.commit()
                flash('Category <b>%s</b> has been edited' % category.name)
                return redirect(url_for('editCategories'))
            else:
                return render_template('editcategory.html', category=category)
        else:
            flash('!E!You are not allowed to edit this category')
            return redirect(url_for('editCategories'))
    else:
        flash('!E!You must log in first')
        return redirect(url_for('login'))


@app.route('/category/<int:category_id>/clear/', methods=['POST', 'GET'])
@helpers.category_exists
def clearCategory(category_id):
    # Require login
    if 'username' in login_session:
        category = session.query(Category).filter_by(id=category_id).one()
        # See if user is category creator
        if login_session['user_id'] == category.user.id:
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
        else:
            flash('!E!You are not allowed to clear this category')
            return redirect(url_for('editCategories'))
    else:
        flash('!E!You must log in first')
        return redirect(url_for('login'))


@app.route('/category/<int:category_id>/delete/', methods=['POST', 'GET'])
@helpers.category_exists
def deleteCategory(category_id):
    # Require login
    if 'username' in login_session:
        category = session.query(Category).filter_by(id=category_id).one()
        # See if user is category creator
        if login_session['user_id'] == category.user.id:
            if request.method == 'POST':
                items = session.query(Item).filter_by(category=category).all()
                for item in items:
                    session.delete(item)
                session.delete(category)
                session.commit()
                flash('Category <b>%s</b> has been deleted' % category.name)
                return redirect(url_for('editCategories'))
            else:
                return render_template('deletecategory.html',
                                       category=category)
        else:
            flash('!E!You are not allowed to delete this category')
            return redirect(url_for('editCategories'))
    else:
        flash('!E!You must log in first')
        return redirect(url_for('login'))


@app.route('/category/<int:category_id>/item/<int:item_id>/')
@helpers.category_exists
@helpers.item_exists
def viewItem(item_id, category_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('viewitem.html', item=item)


@app.route('/item/new/', methods=['POST', 'GET'])
def newItem():
    # Require login
    if 'username' in login_session:
        if request.method == 'POST':
            name = request.form['name']
            if request.form['random-img']:
                picture = get_image.randomImage(name)
            else:
                picture = request.form['picture'].encode("utf-8")
            item = Item(name=name,
                        description=request.form['description'],
                        picture=picture,
                        category_id=request.form['category'],
                        user_id=login_session['user_id'])
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
    else:
        flash('!E!You must log in first')
        return redirect(url_for('login'))


@app.route('/category/<int:category_id>/item/<int:item_id>/edit/',
           methods=['POST', 'GET'])
@helpers.category_exists
@helpers.item_exists
def editItem(item_id, category_id):
    # Require login
    if 'username' in login_session:
        item = session.query(Item).filter_by(id=item_id).one()
        # See if user is item creator or item's category creator
        if (login_session['user_id'] == item.user.id or
                login_session['user_id'] == item.category.user.id):
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
        else:
            flash('!E!You are not allowed to edit this item')
            return redirect(url_for('viewItem',
                                    category_id=category_id,
                                    item_id=item_id))
    else:
        flash('!E!You must log in first')
        return redirect(url_for('login'))


@app.route('/category/<int:category_id>/item/<int:item_id>/delete/',
           methods=['POST', 'GET'])
@helpers.category_exists
@helpers.item_exists
def deleteItem(item_id, category_id):
    # Require login
    if 'username' in login_session:
        item = session.query(Item).filter_by(id=item_id).one()
        # See if user is item creator or item's category creator
        if (login_session['user_id'] == item.user.id or
                login_session['user_id'] == item.category.user.id):
            if request.method == 'POST':
                session.delete(item)
                session.commit()
                flash('Item <b>%s</b> has been deleted' % item.name)
                return redirect(url_for('viewCategory',
                                        category_id=item.category_id))
            else:
                return render_template('deleteitem.html', item=item)
        else:
            flash('!E!You are not allowed to edit this item')
            return redirect(url_for('viewItem',
                                    category_id=category_id,
                                    item_id=item_id))
    else:
        flash('!E!You must log in first')
        return redirect(url_for('login'))


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
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Category=category.serialize(items))


@app.route('/login/')
def login():
    state = helpers.generateState()
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(
            'Invalid state parameter'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange client token for long-lived server-side token
    app_id = json.loads(open(
        'fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open(
        'fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    # Strip expire tag from access token
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['access_token'] = token

    # Get user picture
    url = "https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200" % token  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # Create user, if it doesn't already exist
    user_id = helpers.getUserID(login_session['email'])
    if not user_id:
        user_id = helpers.createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h3>Welcome, '
    output += login_session['username']
    output += '!</h3>'
    output += '<img src="'
    output += login_session['picture']
    output += '" style="width: 200px; height: 200px; border-radius: 50%;">'
    flash('You are now logged in as %s (%s)' % (
        login_session['username'], login_session['email']))
    return output


def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    h.request(url, 'DELETE')[1]


@app.route('/logout/')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['provider']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        flash('You have successfully been logged out')
    else:
        flash('!E!You weren\'t logged in to begin with')
    return redirect(url_for('front'))


if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
