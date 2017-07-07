#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.setup.app import app
from functools import wraps
from database_setup import Category, Item, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import flash, redirect, url_for
import random
import string


engine = create_engine('sqlite:///itemcatalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


def category_exists(f):
    """
    Decorator to see if category exists.
    If not, flash message and redirect to front page
    """
    @wraps(f)
    def wrapper(**kw):
        category = session.query(Category).filter_by(
            id=kw['category_id']).count()
        if category > 0:
            return f(**kw)
        else:
            flash("!E!The category ID (%s) does not exist" % kw['category_id'])
            return redirect(url_for('front'))
    return wrapper


def item_exists(f):
    """
    Decorator to see if item exists.
    If not, flash message and redirect to category page
    """
    @wraps(f)
    def wrapper(**kw):
        item = session.query(Item).filter_by(id=kw['item_id']).count()
        if item > 0:
            return f(**kw)
        else:
            flash("!E!The item ID (%s) does not exist" % kw['item_id'])
            return redirect(url_for('viewCategory',
                                    category_id=kw['category_id']))
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
