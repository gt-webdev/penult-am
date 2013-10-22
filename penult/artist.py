from flask import request, redirect, url_for, abort, render_template
from penult import app
from penult.models import Artist, db

@app.route('/artists')
@app.route('/')
def artists():
  artists = Artist.query.all()
  return render_template('artists.html', artists=artists)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  if artist:
    return render_template('artist.html', artist=artist)

@app.route('/artists', methods=["POST"])
def create_artist():
  # validate form
  name = request.form["name"]
  age = int(request.form["age"])
  bio = request.form["bio"]
  # if valid, create artist and redirect to that artist's page
  if None not in [name, age, bio]:
    artist = Artist(name=name, age=age, bio=bio)
    db.session.add(artist)
    db.session.commit()
    artist_id = artist.id
    return redirect('/artists/%r' % artist_id, code=303)
  return abort(500)

@app.route('/artists/<int:artist_id>', methods=["PUT"])
def update_artist(artist_id):
  # validate form
  artist = Artist.query.get(artist_id)

  if (request.form.get("name", None) != None):
    artist.name = request.form["name"]

  if (request.form.get("age", None) != None):
    if (request.form['age'].isdigit()):
      artist.age = request.form["age"]

  if (request.form.get("bio", None) != None):
    artist.bio = request.form["bio"]

  db.session.add(artist)
  db.session.commit()
  return redirect('/artists/%r' % artist_id, code=303)

@app.route('/artists/<int:artist_id>', methods=["DELETE"])
def delete_artist(artist_id):
  Artist.query.filter_by(id = artist_id).delete()
  return redirect(url_for('artists'), code=303)
