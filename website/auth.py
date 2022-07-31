from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if ( request.method == 'POST' ):
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')

        if ( len(email) < 5 ): #email needs at least 5 characters
            flash('Email seem to be Not Valide', category='error')
        elif ( password != confirm_password  ):
            flash('Passwords Does Not Match', category='error')
        else:
            flash('All seems fine', category='success')

    elif ( request.method == 'GET' ):
        pass
    else:
        pass

    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<h1>logout</h1>"

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
        elif ( len(first_name) < 3 ):
            flash('First Name must contain at lest 3 characters', category='error')
        elif ( len(second_name) < 3 ):
            flash('Second Name must contain at lest 3 characters', category='error')
        elif ( password != confirm_password  ):
            flash('Passwords Does Not Match', category='error')
        else:
            flash('All seems fine', category='success')

    elif ( request.method == 'GET' ):
        pass
    else:
        pass

    return render_template("sign_up.html")