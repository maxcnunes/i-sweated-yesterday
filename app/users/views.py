# third party imports
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort
from werkzeug import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy.sql import or_


# local application imports
from app import db, facebook
from app.users.forms import RegisterForm, LoginForm, RecoverPasswordForm
from app.users.models import User
from app.users.requests import app_before_request
from app.users.decorators import requires_login, redirect_to_profile_logged_users
from app.users.constants import SESSION_NAME_USER_ID
from app.exercises.models import Exercise
from app.users.notifications import send_email_to_recover_user_password

mod = Blueprint('users', __name__, url_prefix='/users')


@mod.before_request
def before_request():
    app_before_request()


@mod.route('/')
@mod.route('/me/')
@requires_login
def index():
    return render_template('users/profile.html', user=g.user)


# @mod.route('/login/', methods=['GET', 'POST'])
# @redirect_to_profile_logged_users
# def login():
#   form = LoginForm(request.form)

#   # make sure data are valid, but doesn't validate password is right
#   if form.validate_on_submit():
#       user = User.query.filter_by(email=form.email.data).first()
#       # we use werzeug to validate user's password
#       if user and check_password_hash(user.password, form.password.data):
#           # the session can't be modified as it's signed,
#           # it's a safe place to store the user id
#           session[SESSION_NAME_USER_ID] = user.id
#           flash('Welcome %s' % user.name)
#           return redirect(url_for('users.index'))
#       flash('Wrong email or password', 'error-message')
#   return render_template( 'users/login.html', form=form)


# @mod.route('/recover_password/', methods=['GET', 'POST'])
# @redirect_to_profile_logged_users
# def recover_password():
#     form = RecoverPasswordForm(request.form)

#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             send_email_to_recover_user_password(form.email.data)
#             flash('Email sent with your password recovery')
#             return redirect(url_for('users.login'))
#         else:   
#             flash('Wrong email', 'error-message')
            
#     return render_template('users/recover_password.html', form=form)


# @mod.route("/recover_password_key/<key>", methods=['GET'])
# def recover_password_key(key):
#     # get user by key
#     user = User.query.filter_by(key_recover_password=key).first()

#     if(user is None):
#         flash('Operation not allowed')
#         return abort(404)

#     # the user verification is ok, then we can login him
#     session[SESSION_NAME_USER_ID] = user.id

#     # reset key and commit changes
#     user.key_recover_password = None
#     db.session.commit()

#     # display a message to the user
#     flash('To complete the password recovery, choose a new password and save it')

#     return redirect(url_for('users.edit'))


@mod.route('/register/', methods=['GET', 'POST'])
@redirect_to_profile_logged_users
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():

        userRegistered = User.query.filter(or_(User.name == form.name.data,\
                                                User.email == form.email.data)).first()
        if userRegistered is not None:
            flash('Email or user already is registered')
            return render_template('users/register.html', form=form)

        # create an user instance not yet stored in the database
        user = User.CreateUser(form.name.data, form.email.data,\
                        generate_password_hash(form.password.data),\
                        form.receive_email_notification.data)

        # insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()

        # log the user in, as he now has an id
        session[SESSION_NAME_USER_ID] = user.id

        # flash will display a message to the user
        flash('Thanks for registering')

        # redirect user to the 'index' method of the user module
        return redirect(url_for('users.index'))
    return render_template('users/register.html', form=form)

@mod.route('/edit/', methods=['GET', 'POST'])
@requires_login
def edit():
    form = RegisterForm(request.form)

    if request.method == 'GET':
        form.name.data = g.user.name
        form.email.data = g.user.email
        form.receive_email_notification.data = g.user.receive_email_notification

    if form.validate_on_submit():

        userRegistered = User.query.filter(or_(User.name == form.name.data,\
                                                User.email == form.email.data))\
                                    .filter(User.id != g.user.id)\
                                    .first()

        # verify if this email or user is alredy used
        if userRegistered is not None:
            flash('Email or user already is registered for another person')
            return render_template('users/edit.html', form=form)

        # get user from the database
        user = User.query.get(g.user.id)

        # update values
        user.name = form.name.data
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)
        user.receive_email_notification = form.receive_email_notification.data

        # update the record in our database and commit it
        db.session.commit()

        # flash will display a message to the user
        flash('User edited successfully')

        # redirect user to the 'index' method of the user module
        return redirect(url_for('users.index'))
    return render_template('users/edit.html', form=form)

@mod.route('/logout/', methods=['GET'])
def logout():
    # remove the username from the session if it's there
    session.pop(SESSION_NAME_USER_ID, None)

    # flash will display a message to the user
    flash('Do not forget keep the exercises')

    # redirect user to the 'index' method of the user module
    return redirect(url_for('users.login'))


@mod.route('/my_reports', methods=['GET'])
@requires_login
def my_reports():
    return render_template('users/my_reports.html')


# FACEBOOK

@mod.route('/login/')
@redirect_to_profile_logged_users
def login():
  return render_template('users/login.html')


@mod.route('/login/facebook')
def login_facebook():
    return facebook.authorize(callback=url_for('users.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@mod.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')

    user = User.create_or_update_user_from_oauth(\
            name=me.data['name'], 
            username=me.data['username'], 
            email=me.data['email'], 
            oauth_key=me.data['id'])

    session[SESSION_NAME_USER_ID] = user.id
    flash('Welcome %s' % user.name)
    return redirect(url_for('users.index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')