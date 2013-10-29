from flask import request, redirect, url_for, abort, render_template
from penult import app
from penult.models import Song, Album, db

@app.route('/songs')
@app.route('/')
def songs():
  songs = Song.query.all()
  return render_template('songs.html', songs=songs)

@app.route('/songs/<int:song_id>')
def show_song(song_id):
  song = Song.query.get(song_id)
  if song:
    return render_template('song.html', song=song)

@app.route('/songs', methods=["POST"])
def create_song():
  # validate form
  name = request.form["name"]
  length = int(request.form["length"])
  album_id = int(request.form["album_id"])
  album = Album.query.get(album_id)
  # if valid, create song and redirect to that song's page
  if None not in [name, length, album]:
    song = Song(name=name, length=length, album=album)
    db.session.add(song)
    db.session.commit()
    song_id = song.id
    return redirect('/songs/%r' % song_id, code=303)
  return abort(500)

@app.route('/songs/<int:song_id>', methods=["PUT"])
def update_song(song_id):
  # validate form
  song = Song.query.get(song_id)

  if (request.form.get("name", None) != None):
    song.name = request.form["name"]

  if (request.form.get("length", None) != None):
    if (request.form['length'].isdigit()):
      song.length = request.form["length"]

  db.session.add(song)
  db.session.commit()
  return redirect('/songs/%r' % song_id, code=303)

@app.route('/songs/<int:song_id>', methods=["DELETE"])
def delete_song(song_id):
  Song.query.filter_by(id = song_id).delete()
  return redirect(url_for('songs'), code=303)
