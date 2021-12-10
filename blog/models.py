from blog import db, login, PasswordSerializer
from sqlalchemy.orm import backref
from datetime import datetime as dt
from flask_login import UserMixin
from flask import current_app

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    email_confirmed = db.Column(db.Boolean(), nullable = False, default = False)
    password = db.Column(db.String(60), nullable = False)
    image_file = db.Column(db.String(25), nullable = False, default = 'default.jpg')
    posts = db.relationship('Post', backref="author", lazy=True)

    def get_token(self):
        s = PasswordSerializer(current_app.config['SECRET_KEY'], 600)
        return s.dumps(self.email).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = PasswordSerializer(current_app.config['SECRET_KEY'])
        try:
            returned_email = s.loads(token)
        except:
            return None
        return User.query.filter_by(email = returned_email).first()

    def __repr__(self):
        return f'Username: {self.username}, Email: {self.email}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = dt.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f'Title: {self.title}, Date Posted: {self.date}'