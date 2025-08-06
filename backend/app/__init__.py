from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    CORS(app)

    # 导入并注册 Blueprints
    from app.auth.routes import auth_bp
    from app.booking.routes import booking_bp
    from app.payment.routes import payment_bp
    from app.sessions.routes import sessions_bp
    from app.members.routes import members_bp
    from app.memberships.routes import memberships_bp
    from app.errors.handlers import errors_bp
    from app.membership_type.routes import membership_type_bp
    app.register_blueprint(membership_type_bp, url_prefix='/api/membership-type')

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(booking_bp, url_prefix='/api/booking')
    app.register_blueprint(payment_bp, url_prefix='/api/payment')
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(members_bp, url_prefix='/api/members')
    app.register_blueprint(memberships_bp, url_prefix='/api/memberships')
    app.register_blueprint(errors_bp)  # 通用错误处理，无需 url_prefix

    # Flask-Login 用户加载器
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.member import Member
        return Member.query.get(int(user_id))

    return app