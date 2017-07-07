from modules.setup.app import app, session
from modules.setup.database import Category, Item
from modules import helpers
from flask import (render_template, redirect, url_for, request,
                   flash, session as login_session)


@app.route('/category/<int:category_id>/delete/', methods=['POST', 'GET'])
@helpers.login_required
@helpers.category_exists
def deleteCategory(category_id):
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
