from flask import Flask
from flask_session import Session
from werkzeug.exceptions import HTTPException, InternalServerError
from src.auth import auth, login_required
from src.helpers import UserInfo, error
from src.profile import profile
from src.search import search
from src.home import home

app = Flask(__name__)
app.config.from_object("config")

app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(profile, url_prefix="/")
app.register_blueprint(home, url_prefix="/")
app.register_blueprint(search, url_prefix="/")

Session(app)
        
@app.errorhandler(Exception)
def errorhandler(e):
    print(str(e))
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)

if __name__ == "__main__":
    app.run()