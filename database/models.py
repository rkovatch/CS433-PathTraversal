from datetime import datetime
from mongoengine import *


class User(Document):
    username = StringField(required=True)
    display_name = StringField(required=True)
    password_hash = StringField(required=True)
    photo_filename = StringField()
    is_admin = BooleanField(default=False)


class Post(Document):
    author = ReferenceField(User, required=True)
    post_text = StringField(required=True)
    date_posted = DateTimeField(default=datetime.now)
