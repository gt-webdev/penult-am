from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.auth import Auth, login_required, logout
from flaskext.auth.models.sa import get_user_class
from penult import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
auth = Auth(app, login_url_name='login')

app.secret_key = "lolsekret"

association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')))

User = get_user_class(db.Model)
User.songs_liked = db.relationship("Song", secondary=association_table)

class Artist(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  age = db.Column(db.Integer)
  bio = db.Column(db.Text)
  albums = db.relationship('Album', backref='artist')

  def __init__(self, name, age, bio):
    self.name = name
    self.age = age
    self.bio = bio

  def __repr__(self):
    return '<Artist %r>' %self.name


class Album(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  year = db.Column(db.Integer)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
  songs = db.relationship('Song', backref='album')


  def __init__(self, name, year, artist):
    self.name = name
    self.year = year
    self.artist_id = artist.id

  def __repr__(self):
    return '<Album %r>' %self.name

class Song(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  length = db.Column(db.Integer)
  album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

  def __init__(self, name, length, album):
    self.name = name
    self.length = length
    self.album_id = album.id

  def __repr__(self):
    return '<Song %r>' %self.name

