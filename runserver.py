from penult import app
from penult.models import db
from method_override import HttpMethodOverrideMiddleware

app.wsgi_app = HttpMethodOverrideMiddleware(app.wsgi_app)

try:
  open('penult/database.db')
except IOError:
  db.create_all()
  
app.run(debug=True)
