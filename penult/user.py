from flask import request, redirect, url_for, abort, render_template, session
from penult import app
from penult.models import User

@app.route('/users/<int:user_id>')
def show_user(user_id):
  user = User.query.get(user_id)
  if user != None:
    return render_template('user.html', user=user)
  return abort(404)

