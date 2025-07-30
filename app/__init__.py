from flask import Flask
from app.config import Config
from extensions import db, login_manager

# ✅ Blueprint Imports
from app.routes import main, register, admin, export

def create_app():
    app = Flask(__name__)  # Fixed typo: name instead of name
    app.config.from_object(Config)

    # ✅ Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # ✅ Set login view
    login_manager.login_view = 'admin.admin_login'

    # ✅ Load user (after db is initialized)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Safe to import here
        return User.query.get(int(user_id))

    # ✅ Register Blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(export.bp)

    return app