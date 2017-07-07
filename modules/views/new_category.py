from modules.setup.app import app, session
from modules.setup.database import Category
from modules import helpers
from flask import (render_template, request, flash, redirect,
                   url_for, session as login_session)


@app.route('/category/new/', methods=['POST', 'GET'])
@helpers.login_required
def newCategory():
    if request.method == 'POST':
        category = Category(name=request.form['name'],
                            user_id=login_session['user_id'])
        session.add(category)
        session.commit()
        flash('Category <b>%s</b> added' % category.name)
        return redirect(url_for('viewCategory', category_id=category.id))
    return render_template('newcategory.html')
