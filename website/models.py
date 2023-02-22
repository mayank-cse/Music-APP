from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

# Db model
class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_title = db.Column(db.String(30), nullable=False)
    track_artist = db.Column(db.String(30), nullable=False)
    track_location = db.Column(db.String(130), nullable=False)
    track_duration = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Track: {}>'.format(self.track_title)