from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.secret_key = secrets.token_hex(16)
    DATABASE_URL = 'postgresql://mydbrender_user:xOn60JTXokZtXCxZIdCjB7Tkx9ysl90G@dpg-coaqgjn109ks73dv5a5g-a/mydbrender'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

    db.init_app(app)

    from .views import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix = '/')

    return app
