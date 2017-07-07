from modules.setup.app import app, session
from modules import get_image, helpers
from flask import (render_template, redirect, url_for, request,
                   flash, session as login_session)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit/',
           methods=['POST', 'GET'])
@helpers.login_required
@helpers.category_exists
@helpers.item_exists
def editItem(item_id, category_id, category, item):
    # See if user is item creator or item's category creator
    if (login_session['user_id'] == item.user.id or
            login_session['user_id'] == item.category.user.id):
        if request.method == 'POST':
            item.name = request.form['name']
            item.description = request.form['description']
            if len(request.form.getlist('random-img')) > 0:
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
            return render_template('edititem.html', item=item)
    else:
        flash('!E!You are not allowed to edit this item')
        return redirect(url_for('viewItem',
                                category_id=category_id,
                                item_id=item_id))
