from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @app.route('/hello')
    def hello():
        return "Goodbye World!"

    from app.models import User

    @login_manager.request_loader
    def load_user_from_request(request):
        api_key = request.args.get('api_key')
        if api_key:
            user = User.query.filter_by(api_key=api_key).first()
            if user:
                login_user(user)
                return user
        return None

    from .apis.tweets import api as tweets
    from .apis.users import api as users
    from .apis.login import api as login

    api = Api()
    api.add_namespace(tweets)
    api.add_namespace(users)
    #api.add_namespace(login)
    api.init_app(app)

    app.config['ERROR_404_HELP'] = False
    return app
