from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('error.html', error_code=404, error_message="That page is unavailable.")

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('error.html', error_code=403, error_message="You do not have the permission to access that page.")

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('error.html', error_code=500, error_message="A server error occured.")