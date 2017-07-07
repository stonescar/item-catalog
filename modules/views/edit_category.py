from modules.setup.app import app, session
from modules import helpers
from flask import (render_template, redirect, url_for, request,
                   flash, session as login_session)


@app.route('/category/<int:category_id>/edit/', methods=['POST', 'GET'])
@helpers.login_required
@helpers.category_exists
def editCategory(category_id, category):
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
