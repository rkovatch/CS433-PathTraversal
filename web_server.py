import os
from os import environ as env
from flask import Flask, request, render_template, abort, redirect, send_file, url_for
from flask_simplelogin import SimpleLogin, get_username, login_required
from database.seeder import seed_db
from database.models import *

app = Flask(__name__)
app.config["SECRET_KEY"] = env["SECRET_KEY"]


def authenticate(user: dict[str, str]) -> bool:
    try:
        found_user = User.objects.get(username=user["username"])
    except DoesNotExist:
        return False
    return found_user.password_hash == hex(hash(user["password"]))


SimpleLogin(app, login_checker=authenticate)

# Connect MongoEngine to mongodb
connect(host=f"mongodb://{env['MONGODB_HOSTNAME']}:27017/socialdb")
if Post.objects.count() == 0:
    seed_db()

@app.route("/")
@login_required
def index():
    return redirect(url_for("home_feed"))


@app.route("/home")
@login_required
def home_feed():
    return render_template("index.html", posts=Post.objects,
                           current_user=User.objects.get(username=get_username()))


@app.route("/delete_post", methods=["POST"])
@login_required
def delete_post():
    post_id = request.form["post_id"]
    try:
        post_to_del = Post.objects.get(pk=post_id)
    except DoesNotExist:
        abort(404)
    if post_to_del.author.username == get_username() or User.objects.get(username=get_username()).is_admin:
        post_to_del.delete()
        return redirect(url_for("home_feed"))
    else:
        abort(403)


@app.route("/profile", methods=["POST"])
@login_required
def update_profile():
    this_user = User.objects.get(username=get_username())
    if request.form["display_name"] != this_user.display_name:
        this_user.display_name = request.form["display_name"]
        this_user.save()
    if "photo" in request.files:
        photo_file = request.files["photo"]
        os.makedirs("photos", exist_ok=True)
        photo_file.save(f"./photos/{photo_file.filename}")  # Vulnerable!
        this_user.photo_filename = photo_file.filename
        this_user.save()
    return redirect(url_for("home_feed"))


@app.route("/get_photo", methods=["GET"])
def get_photo():
    os.makedirs("photos", exist_ok=True)
    photo_filename = request.args.get("file")
    if not photo_filename:
        print('No file arg')
        abort(400)
    photo_path = f"./photos/{photo_filename}"  # Vulnerable!
    if not os.path.isfile(photo_path):
        print('File not found')
        abort(404)
    print('Serving file:', photo_filename)
    return send_file(photo_path)  # Vulnerable!
