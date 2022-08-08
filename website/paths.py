import json
import time

from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from .models import user, note
from .models import db_detail

db = db_detail['db']
DB_NAME = db_detail['DB_NAME']

paths = Blueprint('paths', __name__)

@paths.route('/login', methods=['GET','POST'])
def login():
    if ( request.method == 'POST' ):
        email = request.form.get('email')
        password = request.form.get('password')

        if ( len(email) < 5 ): #email needs at least 5 characters
            flash('Email seem to be Not Valide', category='error')
        elif ( len(password) < 4 ):
            flash('Passwords too small', category='error')
        else:
            user_now = user.query.filter_by(email=email).first()
            if ( user_now ):
                if ( check_password_hash(user_now.password, password) ):
                    login_user(user_now, remember=False)
                    flash('Logging Success', category='success')
                    #time.sleep(0.2)    # Pause 5.5 seconds
                    return redirect(url_for('paths.home'))
                else:
                    flash('Logging Failed', category='error')
            else:
                flash('User does not seem to exist', category='error')

    elif ( request.method == 'GET' ): # for security reasons
        pass
    else:
        pass

    return render_template("login.html", user=current_user)

@paths.route('/logout')
@login_required # make sure its loged in
def logout():
    logout_user()
    return redirect(url_for('paths.login')) # 

@paths.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if ( request.method == 'POST' ):
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')

        if ( len(email) < 5 ): #email needs at least 5 characters
            flash('Email seem to be Not Valide', category='error')

            check_user = user.query.filter_by(email=email).first() # check user existance
            if ( check_user ): # already exist
                flash('User already semm to exist')
                return render_template("sign_up.html")

        elif ( len(first_name) < 3 ):
            flash('First Name must contain at lest 3 characters', category='error')
        elif ( len(second_name) < 3 ):
            flash('Second Name must contain at lest 3 characters', category='error')
        elif ( len(password) < 4 ):
            flash('Passwords too small', category='error')
        elif ( password != confirm_password  ):
            flash('Passwords Does Not Match', category='error')
        else:
            new_user = user(email=email, first_name=first_name, second_name=second_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('All seems fine', category='success')
            return redirect(url_for('paths.home'))

    elif ( request.method == 'GET' ): # for security reasons
        pass
    else:
        pass

    return render_template("sign_up.html", user=current_user)

@paths.route('/', methods=['GET', 'POST'])
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

@paths.route('/delete-note', methods=['POST'])
def delete_note():
    note_received = json.loads(request.data)
    note_id = note_received['note_id']
    note_to_delete = note.query.get(note_id)
    if ( note_to_delete ):
        if ( note_to_delete.user_id == current_user.id ):
            db.session.delete(note_to_delete)
            db.session.commit()
            flash('Note Deleted', category='success')
    else:
        flash('Note seems to not exist', category='error')
    
    return jsonify({})
    #return render_template("home.html", user=current_user)

#----------------------------------------------------------------------
@paths.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@paths.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500