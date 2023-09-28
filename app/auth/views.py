from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from .forms import LoginForm, RegistrationForm, PasswordForm
from .. import db
from ..emails import send_async
from ..models import User


@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if not form.validate_on_submit():
        flash('User already exist or information incorrect')
        return render_template('auth/register.html', form=form)
    else:
        user = User(email=form.email.data, first_name=form.firstname.data,
                    last_name=form.lastname.data, password=form.password.data, phone=form.phone.data,
                    country=form.country.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_async(user.email, 'Confirm Your Account', 'auth/email/confirm.html', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('main.user', name=user.first_name))
            # if next_url is None or not next_url.startswith('/'):
            #     next_url = url_for('main.index')
            # return redirect(next_url)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_async(current_user.email, 'Confirm Your Account', 'auth/email/confirm.html', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed and request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template("auth/unconfirmed.html")


@auth.route('/password_change', methods=["GET", "POST"])
@login_required
def password_change():
    form = PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            flash('Password has been updated!', 'success')
            return redirect(url_for("main.user", name=current_user.first_name))
    return render_template('auth/password_change.html', form=form)
