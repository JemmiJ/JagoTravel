from flask import Flask,jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .models import db, User 
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import stripe


BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    static_folder=os.path.join(BASEDIR, 'static'),
    static_url_path='/static'
)
app.config.from_object(Config)  

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
if not stripe.api_key:
    raise RuntimeError("STRIPE_SECRET_KEY not set in environment")

print("UPLOAD_FOLDER:", app.config['UPLOAD_FOLDER'])
CORS(app, supports_credentials=True)
db.init_app(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

# Flask-Login login manager
jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/api/auth/login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

from app import views  # Import views after initializing app and db to avoid circular imports