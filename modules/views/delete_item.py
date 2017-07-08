from modules.setup.app import app, session
from modules import helpers
from flask import render_template, redirect, url_for, request, flash


@app.route('/category/<int:category_id>/item/<int:item_id>/delete/',
           methods=['POST', 'GET'])
@helpers.login_required
@helpers.csrf_protect
@helpers.category_exists
@helpers.item_exists
@helpers.check_permission
def deleteItem(category_id, category, item_id, item):
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item <b>%s</b> has been deleted' % item.name)
        return redirect(url_for('viewCategory',
                                category_id=item.category_id))
    else:
        return render_template('deleteitem.html', item=item)
