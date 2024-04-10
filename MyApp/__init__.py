from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.secret_key = secrets.token_hex(16)
    DATABASE_URI ='postgresql://mydbrender_user:password@dpg-coaqgjn109ks73dv5a5g-a/mydbrender'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
