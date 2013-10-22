from flask.ext.sqlalchemy import SQLAlchemy
from penult import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Artist(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  age = db.Column(db.Integer)
  bio = db.Column(db.Text)

  def __init__(self, name, age, bio):
    self.name = name
    self.age = age
    self.bio = bio

  def __repr__(self):
    return '<Artist %r>' %self.name
