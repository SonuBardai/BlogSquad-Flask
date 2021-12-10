import os
import json
from blog.user.forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from flask import request, redirect, flash, render_template, url_for, Markup, Blueprint, current_app
from blog.models import User
from blog.user.forms import RegisterForm, ResetPasswordEmail, ResetPassword,User_Info
from blog.user.utils import save_image, send_reset_email
from blog.models import Post
from blog import db, enc, email_serializer

user = Blueprint('user', __name__)

# LOGIN
@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and enc.check_password_hash(user.password, form.password.data): 
            login_user(user, remember = form.remember.data)
            if current_user.email_confirmed:
                flash(f'Successfully logged in as {form.username.data}', 'success')
            if request.args.get('next'): return redirect(request.args.get('next'))
            return redirect(url_for('main.home'))
        else: 
            flash(f'Login failed. Please check your username and password.', 'danger')
            return redirect('/login')
        
    return render_template('login.html', title="Login", form=form)

# LOGOUT
@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# REGISTER
@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))            
    form = RegisterForm()
    if form.validate_on_submit():
        getUsername = form.username.data
        getEmail = form.email.data
        getPassword = form.password.data
        getPassword = enc.generate_password_hash(getPassword).decode('utf-8')
        user = User(username = getUsername, email = getEmail, password = getPassword)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully! Please login to continue.', 'success')
        return redirect('/login')
    return render_template('register.html', title="Register", form = form)

# VERIFY EMAIL
@user.route('/verify_mail', methods=['GET', 'POST'])     # START HERE 
@login_required
def confirm_mail():
    email = current_user.email
    token = email_serializer.dumps(email)
    link = url_for('user.confirm_token', token=token, _external=True)
    return render_template('confirm_mail.html', email = email, link = link)

@user.route('/verify_mail/<string:token>')
@login_required
def confirm_token(token):
    if current_user.email_confirmed:
        return redirect('main.home')
    try:
        email = email_serializer.loads(token, max_age=10)
    except:
        flash('The link expired or the token is invalid. Please try again.', 'warning')
        return redirect(url_for('user.confirm_mail'))
    current_user.email_confirmed = True
    db.session.commit()
    flash('Email Verified!', 'success')
    return redirect(url_for('main.home'))

# RESET PASSWORD 
@user.route('/reset_password', methods=['GET', 'POST'])
def reset_password_email():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordEmail()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if not user:
            flash('There is no account with that email.', 'warning')
            return redirect(url_for('user.register'))
        else:
            token = user.get_token()
            link = url_for('user.reset_password', token=token, _external=True)
            # send_reset_email(link, user)      # CALL FUNCTION TO SEND EMAIL FOR PASSWORD RESET
            flash(Markup(f'''<a href="{ link }" class="text-dark">Link</a>'''), 'info')
        return redirect(url_for('user.login'))
    return render_template('reset_password_email.html', form = form)

@user.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_token(token)
    form = ResetPassword()
    if form.validate_on_submit():
        user.password = enc.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash('Password changed successfully! Please login to continue.', 'success')
        return redirect(url_for('user.login'))
    if user:
        return render_template('reset_password.html', form=form)
    else:
        flash('The link has expired, or the token is incorrect. Please try again.', 'warning')
        return redirect(url_for('user.reset_password_email'))


# ACCOUNT INFO
@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = User_Info()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.image.data:
            if current_user.image_file != 'default.jpg':
                os.remove(f'{os.path.join(current_app.root_path, "static/profile_pics", current_user.image_file)}')
            image_name = save_image(form.image.data)
            current_user.image_file = image_name
        db.session.commit()
        flash('Account Updated', 'success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        user = current_user
        image = url_for('static', filename=f'profile_pics/{user.image_file}')
        form.username.data = current_user.username
        form.email.data = current_user.email
        return render_template('account.html', title="Account", user = user, image = image, form = form)

# GET POSTS BY 
@user.route('/account/<string:username>')
def posts_by(username):
    user = User.query.filter_by(username=username).first_or_404()
    image = url_for('static', filename=f'profile_pics/{user.image_file}')
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(per_page=3, page=page)
    return render_template('posts_by.html', title=user.username, user=user, posts=posts, image=image)

# DELETE IMAGE
@user.route('/del_image')
def delete_image():
    if current_user.image_file != 'default.jpg':
        os.remove(f'{os.path.join(current_app.root_path, "static/profile_pics", current_user.image_file)}')
    current_user.image_file = 'default.jpg'
    db.session.commit()
    return redirect(url_for('user.account'))