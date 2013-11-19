from flask import request, redirect, url_for, abort, render_template, session
from penult import app
from penult.models import Album, Artist, User, db
from flaskext.auth import permission_required

@app.route('/albums')
@app.route('/')
def albums():
  albums = Album.query.all()
  return render_template('albums.html', albums=albums)

@app.route('/albums/<int:album_id>')
def show_album(album_id):
  album = Album.query.get(album_id)
  if (session.get('auth_user') != None):
    if album:
      user = User.query.get(session.get('auth_user')['id'])
      return render_template('album.html', album=album, user=user, playlist=False)
  return render_template('album.html', album=album, user=None, playlist=False)

@app.route('/albums', methods=["POST"])
@permission_required(resource='album', action='create')
def create_album():
  # validate form
  name = request.form["name"]
  year = int(request.form["year"])
  artist_id = int(request.form["artist_id"])
  artist = Artist.query.get(artist_id)

  # if valid, create album and redirect to that album's page
  if None not in [name, year, artist]:
    album = Album(name=name, year=year, artist=artist)
    db.session.add(album)
    db.session.commit()
    album_id = album.id
    return redirect('/albums/%r' % album_id, code=303)
  return abort(500)

@app.route('/albums/<int:album_id>', methods=["PUT"])
@permission_required(resource='album', action='update')
def update_album(album_id):
  # validate form
  album = Album.query.get(album_id)

  if (request.form.get("name", None) != None):
    album.name = request.form["name"]

  if (request.form.get("year", None) != None):
    if (request.form['year'].isdigit()):
      album.year = request.form["year"]

  db.session.add(album)
  db.session.commit()
  return redirect('/albums/%r' % album_id, code=303)

@app.route('/albums/<int:album_id>', methods=["DELETE"])
@permission_required(resource='album', action='delet')
def delete_album(album_id):
  Album.query.filter_by(id = album_id).delete()
  db.session.commit()
  return redirect(url_for('albums'), code=303)

@app.route('/albums/<int:album_id>/like', methods=["POST"])
@permission_required(resource='album', action='like')
def like_album(album_id):
  album = Album.query.get(album_id)
  if (session.get('auth_user') != None):
    user = User.query.get(session.get('auth_user')['id'])
    if (user != None):
      try:
        user.albums_liked.remove(album)
      except:
        user.albums_liked.append(album)
      db.session.add(user)
      db.session.add(album)
      db.session.commit()
      return redirect('/albums/%r' % album_id, code=303)
  return abort(400)
