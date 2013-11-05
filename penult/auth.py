from penult import app
from penult.models import User, db
from flask import request, redirect, url_for, abort, render_template
from flaskext.auth import Auth, login_required, logout

original_algorithm = app.auth.hash_algorithm
app.auth.hash_algorithm = lambda to_encrypt: original_algorithm(to_encrypt.encode('utf-8'))

@login_required()
@app.route('/admin')
def admin():
  return 'YOU ARE THE ADMINISTRATOR!'

@app.route('/login', methods=['GET'])
def login():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
  username = request.form['username']
  user = User.query.filter(User.username==username).one()
  if user is not None:
    if user.authenticate(request.form['password']):
      return redirect(url_for('admin'))
    return abort(401)

@app.route("/register")
def register():
  return render_template('register.html')

@app.route("/register", methods=['POST'])
def register_post():
  username = request.form['username']
  if User.query.filter(User.username==username).first():
    return abort(400)
  password = request.form['password']
  user = User(username=username, password=password)
  db.session.add(user)
  db.session.commit()
  return redirect(url_for('login'))

@app.route("/logout")
def logout():
  user_data = logout()
  if user_data is None:
    return abort(400)
  return "successfully logged out!"


