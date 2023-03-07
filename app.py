"""

Start it using: flask run

Components are stored in `static` and `templates`


"""

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route('/index')
def index():
    return render_template("index.html", title="Demo - Password F.M.")


@app.route("/about")
def about():
    return render_template("about.html", title="About - Password F.M.", is_signed_in=True, is_admin=True)


@app.route("/admin")
def admin():
    return render_template("admin.html", title="About - Password F.M.", is_signed_in=True, is_admin=True)


@app.route("/settings")
def settings():
    return render_template("settings.html", title="About - Password F.M.", is_signed_in=True, is_admin=True)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(ssl_context='adhoc')