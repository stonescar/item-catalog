from modules.setup.app import app, session
from modules.setup.database import Item
from modules import helpers
from flask import (render_template, redirect, url_for, request,
                   flash, session as login_session)


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
