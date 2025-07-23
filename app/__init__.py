from flask import Flask
from app.config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # ✅ Load user AFTER db has been initialized
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Safe import here
        return User.query.get(int(user_id))

    login_manager.login_view = 'admin.admin_login'

    # ✅ Register Blueprints
    from app.routes import main, register, admin
    app.register_blueprint(main.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(admin.bp)

    return app
