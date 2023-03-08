"""

Start it using: flask run

Components are stored in `static` and `templates`


"""
import os  # Used to get the .env file

import flask_login
from dotenv import load_dotenv  # Used to load info from the .env file
from flask import Flask, flash, redirect, render_template, request, url_for

from python_scripts.database_controller import (
    is_admin,
    is_locked_out,
    is_only_admin,
    user_exists,
)
from python_scripts.main import (
    add_user_account,
    delete_user,
    is_authenticated,
    unlock_account,
    update_password,
)
from python_scripts.password_checker import password_valid_to_policy_rules
from python_scripts.username_checker import is_valid_username

app = Flask(__name__)

load_dotenv()  # Load the secrets from the .env file
FLASK_SECRET = os.environ.get("FLASK_SECRET")
app.secret_key = "FLASK_SECRET"

# Login Related
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


# Define User Class
class User:
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
    username = request.form.get("username")
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
@app.route("/index")
def index():
    # If they aren't logged in, redirect them.
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for("login"))
    else:
        return render_template(
            "index.html.jinja",
            title="Index",
            username=flask_login.current_user.id,
            admin=flask_login.current_user.admin,
        )


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html.jinja", title="Login")

    # Get the info from the form
    username = request.form["username"]
    pw = request.form["password"]

    if is_authenticated(username, pw):  # Check it
        # Assign
        user = User(username)
        # Set User Info
        user.id = username
        user.admin = is_admin(username)
        flask_login.login_user(user)
        # Return them to /index
        flash("Login successful")
        return redirect(url_for("index"))

    # Tell the user if their account is locked
    if is_locked_out(username):
        flash(
            "Your account has had too many failed login attempts. Your account has been locked contact an "
            "administrator to unlock it."
        )
        return redirect(url_for("login"))

    # Login Failed
    flash("Incorrect username or password combination")
    return redirect(url_for("login"))


@app.route("/about")
def about():
    if flask_login.current_user.is_active:
        return render_template(
            "about.html.jinja",
            title="About",
            username=flask_login.current_user.id,
            admin=flask_login.current_user.admin,
        )
    else:
        return render_template("about.html.jinja", title="About")


@app.route("/protected")
@flask_login.login_required
def protected():
    return "Logged in as admin account: " + str(flask_login.current_user.admin)


@app.route("/admin")
@flask_login.login_required
def admin():
    if flask_login.current_user.admin is True:
        return render_template(
            "admin.html.jinja",
            title="Admin",
            username=flask_login.current_user.id,
            admin=flask_login.current_user.admin,
        )
    else:
        return "You can not be here"


@app.route("/settings")
@flask_login.login_required
def settings():
    return render_template(
        "settings.html.jinja",
        title="Settings",
        username=flask_login.current_user.id,
        admin=flask_login.current_user.admin,
    )


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return render_template("logout.html.jinja", title="Logged Out")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html.jinja"), 404


@app.route("/add_account", methods=["POST"])
def do_add_account():
    if request.method == "POST":
        # Check if admin
        if flask_login.current_user.admin is True:
            new_account_username = request.form["new-username"]
            new_account_password = request.form["password"]
            new_account_confirm_password = request.form["confirm-password"]
            new_account_type = request.form["account-type"]
            requesting_admin_username = flask_login.current_user.id
            requesting_admin_password = request.form["confirm-admin-password-add"]

            # Check the admin password confirmation first
            if is_authenticated(requesting_admin_username, requesting_admin_password) is True:
                # Check if the username is already taken
                if user_exists(new_account_username) is True:
                    flash("The username is already taken.")
                    return redirect(url_for("admin"))

                # Check if username follows the policy
                if is_valid_username(new_account_username) is False:
                    flash("Username doesn't meet the username policy")
                    return redirect(url_for("admin"))

                # Check if the password don't match
                if new_account_password != new_account_confirm_password:
                    flash("Confirmation password does not match the given password.")
                    return redirect(url_for("admin"))

                # Check if password follows the policy
                if password_valid_to_policy_rules(new_account_password) is False:
                    flash("Password doesn't meet the password policy")
                    return redirect(url_for("admin"))

                # Passed the checks
                if new_account_type == "0":
                    add_user_account(
                        requesting_admin_username,
                        requesting_admin_password,
                        new_account_username,
                        new_account_password,
                        add_as_admin=False,
                    )
                    flash(f"Normal user account named: {new_account_username} has been created.")
                elif new_account_type == "1":
                    add_user_account(
                        requesting_admin_username,
                        requesting_admin_password,
                        new_account_username,
                        new_account_password,
                        add_as_admin=True,
                    )
                    flash(f"Admin user account named: {new_account_username} has been created.")
                else:  # This shouldn't be reached, normally.
                    flash("An error: Occurred")
                return redirect(url_for("admin"))

            elif is_locked_out(requesting_admin_username) is True:
                flash("Your admin password was wrong too many times. Your account has been locked.")
                return redirect(url_for("admin"))
            else:
                flash("The admin password is incorrect.")
                return redirect(url_for("admin"))

        # Reject if not admin
        else:
            flash("You don't have the correct permissions.")
            return redirect(url_for("index"))

    # People shouldn't be on this page.
    else:
        return redirect(url_for("index"))


@app.route("/delete_account", methods=["POST"])
def do_delete_account():
    if request.method == "POST":
        # Check if admin
        if flask_login.current_user.admin is True:
            username_delete = request.form["delete-username"]
            confirm_delete_username = request.form["confirm-delete-username"]
            requesting_admin_username = flask_login.current_user.id
            requesting_admin_password = request.form["confirm-admin-password-delete"]

            # Check the admin password confirmation first
            if is_authenticated(requesting_admin_username, requesting_admin_password) is True:
                # Check if they match
                if username_delete != confirm_delete_username:
                    flash("Error: Given username does not match confirmation username")
                    return redirect(url_for("admin"))
                if user_exists(username_delete) is False:
                    flash(f"Error: {username_delete} not exist in the system.")
                    return redirect(url_for("admin"))

                if delete_user(requesting_admin_username, requesting_admin_password, username_delete) is True:
                    flash(f"Success: {username_delete} has been deleted from the system.")
                    return redirect(url_for("admin"))
                else:
                    flash(f"Error: {username_delete} could not be deleted from the system.")
                    if is_admin(username_delete) and is_only_admin():
                        flash(
                            f"Error: You requesting the only admin account to be deleted."
                            f"is_only_admin: {is_only_admin()}"
                        )
                    return redirect(url_for("admin"))

            elif is_locked_out(requesting_admin_username) is True:
                flash("Your admin password was wrong too many times. Your account has been locked.")
                return redirect(url_for("admin"))
            else:
                flash("The admin password is incorrect.")
                return redirect(url_for("admin"))

        # Reject if not admin
        else:
            flash("You don't have the correct permissions.")
            return redirect(url_for("index"))

    # People shouldn't be on this page.
    else:
        return redirect(url_for("index"))


@app.route("/unlock_account", methods=["POST"])
def do_unlock_account():
    if request.method == "POST":
        # Check if admin
        if flask_login.current_user.admin is True:
            username_unlock = request.form["unlock-username"]
            confirm_unlock_username = request.form["confirm-unlock-username"]
            requesting_admin_username = flask_login.current_user.id
            requesting_admin_password = request.form["confirm-admin-password-unlock"]

            # Check the admin password confirmation first
            if is_authenticated(requesting_admin_username, requesting_admin_password) is True:
                # Check if they match
                if username_unlock != confirm_unlock_username:
                    flash("Error: Given username does not match confirmation username")
                    return redirect(url_for("admin"))

                if user_exists(username_unlock) is False:
                    flash(f"Error: {username_unlock} not exist in the system.")
                    return redirect(url_for("admin"))

                if unlock_account(requesting_admin_username, requesting_admin_password, username_unlock) is True:
                    flash(f"Success: {username_unlock} has been unlocked on the system.")
                    return redirect(url_for("admin"))
                else:
                    # This shouldn't be reached.
                    flash(f"Error: {username_unlock} could not be unlocked on the system.")
                    return redirect(url_for("admin"))

            elif is_locked_out(requesting_admin_username) is True:
                flash("Your admin password was wrong too many times. Your account has been locked.")
                return redirect(url_for("admin"))
            else:
                flash("The admin password is incorrect.")
                return redirect(url_for("admin"))

        # Reject if not admin
        else:
            flash("You don't have the correct permissions.")
            return redirect(url_for("index"))

    # People shouldn't be on this page.
    else:
        return redirect(url_for("index"))


@app.route("/change_password", methods=["POST"])
def do_update_password():
    if request.method == "POST":
        username = flask_login.current_user.id
        new_password = request.form["password"]
        confirm_new_password = request.form["confirm-password"]
        confirm_old_password = request.form["confirm-old-password"]
        # Check that they know their old password
        if is_authenticated(username, confirm_old_password) is True:
            # Check if they match
            if new_password != confirm_new_password:
                flash("Error: Updated password does not match confirmation password")
                return redirect(url_for("settings"))

            if password_valid_to_policy_rules(new_password) is True:
                if update_password(username, confirm_old_password, new_password) is True:
                    flash(f"Success: {username}, you have changed your password system.")
                    return redirect(url_for("settings"))
                else:
                    # This shouldn't be reached.
                    flash(f"Error: {username}, you can not change your password on the system.")
                    return redirect(url_for("settings"))
            else:
                flash(f"Error: {username}, your new password does not follow the password policy.")
                return redirect(url_for("settings"))

        elif is_locked_out(username) is True:
            flash("Your password was wrong too many times. Your account has been locked.")
            return redirect(url_for("settings"))
        else:
            flash("Your current password is incorrect.")
            return redirect(url_for("settings"))

    # People shouldn't be on this page.
    else:
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
