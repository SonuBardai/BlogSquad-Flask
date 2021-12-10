class Config:
    SECRET_KEY = '16f2f8f9d3babe48672c575d3d8d225e'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp@googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'admin_email@gmail.com'
    MAIL_PASSWORD = 'admin_password'