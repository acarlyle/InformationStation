# app/home/views.py

from flask import abort, render_template, url_for, redirect
from flask_login import current_user, login_required

from . import home

import datetime

from forms import EmailForm, PasswordForm
from .. import db
from ..models import User, ApplicationInformation
from ..helpers import admin_required
from ..utils import send_email, ts

# Index
@home.route('/')
def index():
    return render_template("home/index.html")
    
    
@home.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"
        print(subject)

        # Here we use the URLSafeTimedSerializer we created in `util` at the
        # beginning of the chapter
        token = ts.dumps(user.email, salt='recover-key')

        recover_url = url_for(
            'home.reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url)

        # Let's assume that send_email was defined in myapp/util.py
        send_email(subject, 'no-reply@coeas', user.email, html)

        return redirect(url_for('home.index'))
    return render_template('home/reset.html', form=form)
    
@home.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('home/reset_with_token.html', form=form, token=token)
    
    
# User Dashboard
@home.route('/dashboard')
@login_required
def dashboard():
    
    print('rendering userdash. . .')
    
    today = datetime.date.today()
    print(today)
    
    #get deadlines from database
    
    query = db.session.query(ApplicationInformation)
    print('querY:', query)
    
    ai = ApplicationInformation.query.all()

    deadlines = []

    for a in ai:
        print a.name, a.deadlineDate
        deadlines.append(a.deadlineDate)
    
    return render_template("home/userdash.html", fifthyeardeadline=deadlines[1], undergraddeadline=deadlines[2], postbacdeadline=deadlines[0], today=today)
    
# @home.route('/admin/dashboard')
# @admin_required
# def admin_dashboard():
#     return render_template('home/admin_dashboard.html', title="Dashboard")