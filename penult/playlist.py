from flask import request, redirect, url_for, abort, render_template, session
from flaskext.auth import login_required, permission_required
from penult import app
from penult.models import Playlist, Album, Song, User, db

@app.route('/playlists/<int:playlist_id>')
def show_playlist(playlist_id):
  playlist = Playlist.query.get(playlist_id)
  if (session.get('auth_user') != None):
    if playlist:
      user = User.query.get(session.get('auth_user')['id'])
      return render_template('album.html', album=playlist, user=user, playlist=True)
    return render_template('album.html', album=playlist, user=None, playlist=True)

@app.route('/playlists', methods=["POST"])
@permission_required(resource='playlist', action='create')
def create_playlist():
  name = request.form["name"]
  if (session.get('auth_user') != None):
    user = User.query.get(session.get('auth_user')['id'])
    if None not in [name, user]:
      playlist = Playlist(name=name, creator=user)
      db.session.add(playlist)
      db.session.commit()
      playlist_id = playlist.id
      redirect_path = request.form.get('redirect')
      if (redirect_path):
        return redirect(redirect_path, code=303)
      return redirect('/playlists/%r' % playlist_id, code=303)
  return abort(500)

@app.route('/playlists/<int:playlist_id>', methods=["DELETE"])
@permission_required(resource='playlist', action='create')
def delete_playlist(playlist_id):
  if (session.get('auth_user') != None):
    user = User.query.get(session.get('auth_user')['id'])
    Playlist.query.filter_by(creator_id=user.id, id = playlist_id).delete()
    db.session.commit()
    return redirect(url_for('artists'), code=303)


@app.route('/playlists/<int:playlist_id>/<add_type>', methods=["POST"])
@permission_required(resource='playlist', action='create')
def add_to_playlist(playlist_id, add_type):
  if add_type == "song":
    song_id = int(request.form['song_id'])
    songs = [Song.query.get(song_id)]
  elif add_type == "album":
    album_id = int(request.form['album_id'])
    songs = Album.query.get(album_id).songs
  else:
    return abort(400)
  playlist = Playlist.query.get(playlist_id)
  for song in songs:
    playlist.songs.append(song)
  db.session.add(playlist)
  db.session.commit()
  return redirect('/playlists/%r' % playlist_id, code=303)
