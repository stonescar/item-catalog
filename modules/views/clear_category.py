from modules.setup.app import app, session
from modules.setup.database import Item
from modules import helpers
from flask import render_template, redirect, url_for, request, flash


@app.route('/category/<int:category_id>/clear/', methods=['POST', 'GET'])
@helpers.login_required
@helpers.category_exists
@helpers.check_permission
def clearCategory(category_id, category):
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
