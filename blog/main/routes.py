from flask import render_template, request, Blueprint
from blog.models import Post
from flask_login import current_user
from blog import db

main = Blueprint('main', __name__)

# HOME
@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(per_page=3, page=page)
    return render_template('index.html', posts = posts)

# ABOUT
@main.route('/about')
def about():
    current_user.email_confirmed = False
    db.session.commit()
    return render_template('about.html', title="About")