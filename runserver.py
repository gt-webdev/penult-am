from penult import app
from method_override import HttpMethodOverrideMiddleware

app.wsgi_app = HttpMethodOverrideMiddleware(app.wsgi_app)
app.run(debug=True)
