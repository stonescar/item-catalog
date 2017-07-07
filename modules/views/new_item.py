from modules.setup.app import app, session
from modules.setup.database import Item
from modules import helpers
from modules import get_image
from flask import (render_template, redirect, url_for, request,
                   flash, session as login_session)


@app.route('/item/new/', methods=['POST', 'GET'])
@helpers.login_required
def newItem():
    if request.method == 'POST':
        name = request.form['name']
        if len(request.form.getlist('random-img')) > 0:
            picture = get_image.randomImage(name)
        else:
            picture = request.form['picture']
        item = Item(name=name,
                    description=request.form['description'],
                    picture=picture,
                    category_id=request.form['category'],
                    user_id=login_session['user_id'])
        session.add(item)
        session.commit()
        flash('Item <b>%s</b> added' % item.name)
        return redirect(url_for('viewCategory',
                                category_id=item.category_id))
    else:
        if request.referrer and 'category' in request.referrer:
            referrer = int(request.referrer.split("/")[4])
            return render_template('newitem.html', ref=referrer)
        else:
            return render_template('newitem.html')
