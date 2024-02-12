from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import socket

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def get_ip_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a remote server (doesn't have to be reachable)
        s.connect(('8.8.8.8', 80))
        # Get the socket's local address, which should be your IP address
        ip_address = s.getsockname()[0]
        return ip_address
    except socket.error:
        return None

if __name__ == "__main__":
    app = create_app()
    ip_address = get_ip_address()
    print(f"Server running on {ip_address}:5000")
    app.run(host=ip_address, port=5000)