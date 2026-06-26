import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config
from .models import db, User

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

CORS(app, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ensures upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from . import views