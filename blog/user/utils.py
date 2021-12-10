import os
import secrets
from PIL import Image
from flask_mail import Message
from blog import mail
from flask import current_app

# PROFILE PICTURE UPDATE FUNCTION
def save_image(image):
    _, ext = os.path.splitext(image.filename)
    hex = secrets.token_hex(8)
    new_name = hex + ext
    new_path = os.path.join(current_app.root_path, 'static/profile_pics', new_name)

    res = (125, 125)

    image_compress = Image.open(image)
    image_compress.thumbnail(res)

    image_compress.save(new_path)
    return new_name

# RESET PASSWORD EMAIL SENDER
def send_reset_email(link, user):
    message = Message('Password Reset Request', sender='noreply@gmail.com', recipients=user.email)
    body = f'''Please follow this link to reset your password. 
{link} 
If you did not make the reset request then please ignore this mail.'''
    mail.send(message)
    return message