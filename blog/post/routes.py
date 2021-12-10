from flask_login import current_user, login_required
from blog.post.forms import PostForm
from blog.models import Post
from werkzeug.utils import redirect
from flask import request, url_for, render_template, abort, flash, Blueprint
from blog import db

posts = Blueprint('posts', __name__)

# CREATE NEW POST
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()    
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        return render_template('userpost.html', title='New Post', form=form, legend="New Post")

# GET A POST
@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

# UPDATE POST
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(f'/post/{post_id}')
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        return render_template('userpost.html', form=form, post=post, legend="Update Post")

# DELETE POST
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Your Post has been deleted', 'success')
        return redirect(url_for('main.home'))