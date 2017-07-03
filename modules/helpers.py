#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from database_setup import Category, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import flash, redirect, url_for


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
