import time
from flask import Blueprint, redirect, render_template, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


from .models import user, notes
from .__init__ import db

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
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
                    flash('All seems fine', category='success')
                    login_user(user_now, remember=False)
                    flash('Logging Success', category='success')
                    #time.sleep(0.2)    # Pause 5.5 seconds
                    return redirect(url_for('views.home'))
                else:
                    flash('Logging Failed', category='error')
            else:
                flash('User does not seem to exist', category='error')

    elif ( request.method == 'GET' ): # for security reasons
        pass
    else:
        pass

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required # make sure its loged in
def logout():
    logout_user()
    return redirect(url_for('auth.login')) # 

@auth.route('/sign-up', methods=['GET','POST'])
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
            return redirect(url_for('views.home'))

    elif ( request.method == 'GET' ): # for security reasons
        pass
    else:
        pass

    return render_template("sign_up.html", user=current_user)