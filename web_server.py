import os

from flask import Flask, request, render_template, abort, redirect, send_file
from flask_simplelogin import SimpleLogin, login_required
from os import environ as env

app = Flask(__name__)
app.config["SECRET_KEY"] = env["SECRET_KEY"]


def authenticate(user: dict[str, str]) -> bool:
    return (user["username"] == "admin" and user["password"] == "banana") or \
           (user["username"] == "bobby" and user["password"] == "hunter2") or \
           (user["username"] == "alice" and user["password"] == "passw0rd")


SimpleLogin(app, login_checker=authenticate)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/profile", methods=["POST"])
def update_profile():
    if 'photo' not in request.files:
        print('No file part')
        abort(400)
    elif request.files['photo'].filename == '':
        print('No selected file')
        abort(400)
    else:
        print('Got file')
        request.files['photo'].save(f"photos/{request.files['photo'].filename}")  # Vulnerable!
        return redirect("/")


@app.route("/get_photo", methods=["GET"])
def get_photo():
    photo_filename = request.args.get("file")
    if not photo_filename:
        print('No file arg')
        abort(400)
    elif not os.path.isfile(f"./photos/{photo_filename}"):
        print('File not found')
        abort(404)
    else:
        print('Got file')
        return send_file(f"./photos/{photo_filename}")  # Vulnerable!
