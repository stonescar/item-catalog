#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.setup.app import app, session
from modules.setup.database import Category, Item, User
from functools import wraps
from flask import flash, redirect, url_for, session as login_session
import random
import string


def category_exists(f):
    """
    Decorator to see if category exists.
    If not, flash message and redirect to front page
    If the category exists, pass the category along
    """
    @wraps(f)
    def wrapper(category_id, item_id=None):
        try:
            category = session.query(Category).filter_by(
                id=category_id).one()
        except:
            flash('!E!The category ID (%s) does not exist' % category_id)
            return redirect(url_for('front'))
        if item_id:
            return f(category_id, item_id, category)
        else:
            return f(category_id, category)
    return wrapper


def item_exists(f):
    """
    Decorator to see if item exists.
    If not, flash message and redirect to category page
    If the item exists, pass the item along
    """
    @wraps(f)
    def wrapper(category_id, item_id, category):
        try:
            item = session.query(Item).filter_by(
                id=item_id).one()
        except:
            flash('!E!The item ID (%s) does not exist' % item_id)
            return redirect(url_for('viewCategory',
                                    category_id=category_id))
        return f(item_id, category_id, category, item)
    return wrapper


def login_required(f):
    """
    Decorator to see if user is logged in.
    If not, flash message and redirect to front page
    """
    @wraps(f)
    def wrapper(**kw):
        if 'username' in login_session:
            return f(**kw)
        else:
            flash('!E!You must log in first')
            return redirect(url_for('login'))
    return wrapper


def check_permission(f):
    """
    Decorator to see if user is allowed to edit post.
    Only category creator can edit, clear or delete category.
    Item creator can edit or delete item. The creator of the category
    the item belongs to can also edit or delete item. In other words:
    The category creator can edit and delete ALL items within the category,
    even the ones not created by him.
    """
    @wraps(f)
    def wrapper(category_id, category, item_id=None, item=None):
        if ((item and
                login_session['user_id'] == item.user.id) or
                login_session['user_id'] == category.user.id):
            if item:
                return f(item_id, category_id, category, item)
            else:
                return f(category_id, category)
        else:
            flash('!E!You don\'t have permission to preform this operation')
            return redirect(url_for('front'))
    return wrapper


# User functions
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    return newUser.id


def generateState():
    state = ''.join(random.choice(
        string.ascii_uppercase+string.digits) for x in xrange(32))
    return state


@app.context_processor
def utility_processor():
    def get_categories():
        categories = session.query(Category).order_by(Category.name).all()
        for c in categories:
            c.count = session.query(Item).filter_by(category_id=c.id).count()
        return categories
    return dict(get_categories=get_categories)
