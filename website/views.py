import json

from flask import Blueprint, render_template , request, flash, jsonify
from flask_login import login_required, current_user

from .__init__ import db_detail
from .models import note

# handling cargo
db = db_detail['db']

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if (request.method == 'POST'):
        new_note = request.form.get('note')
        if ( not new_note ):
            flash('Note seems to be empty', category='error')
        else:
            new_note = note(data=new_note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['note']
    note = note.query.get(note_id)
    if ( note ):
        if ( note.user_id == current_user.id ):
            db.session.delete(note)
            db.session.commit()

    return jsonify({})