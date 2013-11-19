from flask import request, redirect, url_for, abort, render_template, session
from penult import app
from penult.models import Artist, User, db
from flaskext.auth import permission_required, has_permission

@app.route('/artists')
@app.route('/')
def artists():
  artists = Artist.query.all()
  return render_template('artists.html', artists=artists)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  if (session.get('auth_user') != None):
    if artist:
      user = User.query.get(session.get('auth_user')['id'])
      return render_template('artist.html', artist=artist, user=user)
  return render_template('artist.html', artist=artist, user=None)

@app.route('/artists', methods=["POST"])
@permission_required(resource='artist', action='create')
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
@permission_required(resource='artist', action='update')
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
@permission_required(resource='artist', action='delete')
def delete_artist(artist_id):
  Artist.query.filter_by(id = artist_id).delete()
  db.session.commit()
  return redirect(url_for('artists'), code=303)

@app.route('/artists/<int:artist_id>/like', methods=["POST"])
@permission_required(resource='artist', action='like')
def like_artist(artist_id):
  artist = Artist.query.get(artist_id)
  if (session.get('auth_user') != None):
    user = User.query.get(session.get('auth_user')['id'])
    if (user != None):
      try:
        user.artists_liked.remove(artist)
      except:
        user.artists_liked.append(artist)
      db.session.add(user)
      db.session.add(artist)
      db.session.commit()
      return redirect('/artists/%r' % artist_id, code=303)
  return abort(400)
