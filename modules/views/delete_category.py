from modules.setup.app import app, session
from modules.setup.database import Item
from modules import helpers
from flask import render_template, redirect, url_for, request, flash


@app.route('/category/<int:category_id>/delete/', methods=['POST', 'GET'])
@helpers.login_required
@helpers.category_exists
@helpers.check_permission
def deleteCategory(category_id, category):
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
