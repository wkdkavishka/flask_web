from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .models import user, create_database, db_detail

# handling cargo
db = db_detail['db']
DB_NAME = db_detail['DB_NAME']

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'fuck' # encryption
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .paths import paths

    app.register_blueprint(paths, url_prefix='/')

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'paths.login'
    login_manager.init_app(app)

    @login_manager.user_loader # handels login
    def load_user(id):
        return user.query.get(int(id)) # 

    return app
