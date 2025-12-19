from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from mongoengine.fields import StringField, EmailField, FileField, ImageField, ReferenceField
from mongoengine.errors import ValidationError as MongoValidationError


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = StringField(required=True, unique=True, min_length=1, max_length=40)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    profile_pic = ImageField(required=False)

    def get_id(self):
        return self.username


class Review(db.Document):
    commenter = ReferenceField(User, required=True)
    content = StringField(required=True, min_length=5, max_length=500)
    date = StringField(required=True)
    book_id = StringField(required=True)
    book_title = StringField(required=True, min_length=1, max_length=100)