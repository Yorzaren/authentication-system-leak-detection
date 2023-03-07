"""

Start it using: flask run

Components are stored in `static` and `templates`


"""
from flask import Flask, render_template, request, redirect, url_for, flash
import flask_login

from python_scripts.database_controller import is_admin, user_exists
from python_scripts.main import (
    add_user_account,
    delete_user,
    is_authenticated,
    unlock_account,
    update_password,
)

app = Flask(__name__)
app.secret_key = 'secret'  # Change this!

# Login Related
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


# Define User Class
class User():
    def __init__(self, id, admin=False):
        self.id = id
        self.admin = admin

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id


@login_manager.user_loader
def user_loader(username):
    if user_exists(username) is False:
        return

    user = User(username)
    user.id = username
    user.admin = is_admin(username)
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if user_exists(username) is False:
        return

    user = User(username)
    user.id = username
    user.admin = is_admin(username)
    return user


"""if session is not None:
    # Get the session data is it exists
    if "username" in session:
        current_username = session["username"]
    if "signed_in" in session:
        is_signed_in = session["signed_in"]
    if "admin" in session:
        user_is_admin = session["is_admin"]
"""


@app.route("/")
@app.route('/index')
def index():
    # If they aren't logged in, redirect them.
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template("index.html", title="Index", username=flask_login.current_user.id, admin=flask_login.current_user.admin)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template("login.html", title="Login")

    # Get the info from the form
    username = request.form['username']
    pw = request.form['password']

    if is_authenticated(username, pw):  # Check it
        # Assign
        user = User(username)
        # Set User Info
        user.id = username
        user.admin = is_admin(username)
        flask_login.login_user(user)
        # Return them to /index
        flash('Login successful')
        return redirect(url_for('index'))

    return 'Bad login'


@app.route("/about")
def about():
    if flask_login.current_user.is_active:
        return render_template("about.html", title="About", username=flask_login.current_user.id)
    else:
        return render_template("about.html", title="About")


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as admin account: ' + str(flask_login.current_user.admin)


@app.route("/admin")
@flask_login.login_required
def admin():
    if flask_login.current_user.admin is True:
        return render_template("admin.html", title="Admin", username=flask_login.current_user.id)
    else:
        return 'You can not be here'


@app.route("/settings")
@flask_login.login_required
def settings():
    return render_template("settings.html", title="Settings", username=flask_login.current_user.id)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template("logout.html", title="Logged Out")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
