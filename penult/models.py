from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.auth import Auth, login_required, logout, Permission, Role
from flaskext.auth.models.sa import get_user_class
from penult import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
auth = Auth(app)

def create_admin_permissions():
  perms = []
  for resource in ['artist', 'album', 'song']:
    for action in ['create', 'update', 'delete']:
      perms.append(Permission(resource, action))
  return perms

def create_user_premsissions():
  perms = []
  for action in ['create', 'addto', 'delet']:
    perms.append(Permission('playlist', action))
  for resource in ['artist', 'album', 'song']:
    perms.append(Permission(resource, 'like'))
  return perms


roles = {
  'admin': Role('admin', create_admin_permissions() + create_user_premsissions()),
  'user': Role('user', create_user_premsissions())
}

def load_role(role_name):
  return roles.get(role_name)

auth.load_role = load_role

app.secret_key = "lolsekret"

# association tabels used for many-to-many relationships, e.g. "A user likes 
# many songs, but a song may be liked by many users"
association_table_so = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')))
association_table_al = db.Table('association_al', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id')))
association_table_ar = db.Table('association_ar', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')))
songs_to_playlists = db.Table('songs_to_playlists', db.Model.metadata,
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')))


User = get_user_class(db.Model)
User.songs_liked = db.relationship("Song", secondary=association_table_so)
User.albums_liked = db.relationship("Album", secondary=association_table_al)
User.artists_liked = db.relationship("Artist", secondary=association_table_ar)
User.playlists = db.relationship("Playlist", backref='creator')

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

class Playlist(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  songs = db.relationship("Song", secondary=songs_to_playlists)

  def __init__(self, name, creator):
    self.name = name
    self.creator_id = creator.id

  def __repr__(self):
    return '<Playlist %r>' %self.name
