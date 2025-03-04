import os

from flask import Flask, request, render_template, abort, redirect, send_file, url_for
from flask_simplelogin import SimpleLogin, get_username, login_required
from os import environ as env

app = Flask(__name__)
app.config["SECRET_KEY"] = env["SECRET_KEY"]

# Hardcoded accounts (for demonstration only)
accounts = {
    "admin": "banana",
    "bobby": "hunter2",
    "alice": "passw0rd"
}


def authenticate(user: dict[str, str]) -> bool:
    username = user.get("username", "")
    password = user.get("password", "")
    return accounts.get(username) == password


SimpleLogin(app, login_checker=authenticate)


@app.route("/")
@login_required
def index():
    return redirect(url_for("home_feed"))


@app.route("/home")
@login_required
def home_feed():
    return render_template("index.html")


@app.route("/profile", methods=["POST"])
def update_profile():
    if 'photo' not in request.files:
        print('No file part')
        abort(400)
    elif request.files['photo'].filename == '':
        print('No selected file')
        abort(400)

    # Log additional fields (first and last name) for demonstration.
    first_name = request.form.get("fname", "")
    last_name = request.form.get("lname", "")
    print(f"Profile update for {get_username()} – First Name: {first_name}, Last Name: {last_name}")
    os.makedirs("photos", exist_ok=True)
    request.files['photo'].save(f"photos/{request.files['photo'].filename}")  # Vulnerable!
    return redirect(url_for("shopping"))


@app.route("/get_photo", methods=["GET"])
def get_photo():
    os.makedirs("photos", exist_ok=True)
    photo_filename = request.args.get("file")
    if not photo_filename:
        print('No file arg')
        abort(400)
    elif not os.path.isfile(f"./photos/{photo_filename}"):
        print('File not found')
        abort(404)
    print('Serving file:', photo_filename)
    return send_file(photo_filename)
