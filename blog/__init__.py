from flask import Flask, flash, Markup, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer as EmailSerializer, TimedJSONWebSignatureSerializer as PasswordSerializer
from flask_mail import Mail
from blog.config import Config

enc = Bcrypt()
login = LoginManager()
mail = Mail()
db = SQLAlchemy()

email_serializer = EmailSerializer(Config.SECRET_KEY)

login.login_view = 'login'
login.login_message_category = 'info'
login.login_message = 'You need to be logged-in to access your account.'

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    enc.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    
    from blog.user.routes import user
    from blog.post.routes import posts
    from blog.main.routes import main
    from blog.errors.handlers import errors
    app.register_blueprint(user)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app