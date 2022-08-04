from flask import Blueprint, render_template , request, flash
from flask_login import login_required, current_user

from .__init__ import db_detail
from .models import notes

# handling cargo
db = db_detail['db']

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if (request.method == 'POST'):
        note = request.form.get('note')
        if ( not note ):
            flash('Note seems to be empty', category='error')
        else:
            new_note = notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added', category='success')

    return render_template("home.html", user=current_user)