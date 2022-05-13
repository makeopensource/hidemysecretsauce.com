from views.two_factor import two_factor 
from views.login import login
from views.signup import signup
from views.sauce import sauce
from flask import Flask


app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(signup)
app.register_blueprint(two_factor)
app.register_blueprint(sauce)
SECURE = False


