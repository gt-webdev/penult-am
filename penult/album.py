from flask import request, redirect, url_for, abort, render_template
from penult import app
from penult.models import Album, db

@app.route('/albums')
@app.route('/')
def albums():
  albums = Album.query.all()
  return render_template('albums.html', albums=albums)

@app.route('/albums/<int:album_id>')
def show_album(album_id):
  album = Album.query.get(album_id)
  if album:
    return render_template('album.html', album=album)

@app.route('/albums', methods=["POST"])
def create_album():
  # validate form
  name = request.form["name"]
  year = int(request.form["year"])
  # if valid, create album and redirect to that album's page
  if None not in [name, year]:
    album = Album(name=name, year=year)
    db.session.add(album)
    db.session.commit()
    album_id = album.id
    return redirect('/albums/%r' % album_id, code=303)
  return abort(500)

@app.route('/albums/<int:album_id>', methods=["PUT"])
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
def delete_album(album_id):
  Album.query.filter_by(id = album_id).delete()
  return redirect(url_for('albums'), code=303)
