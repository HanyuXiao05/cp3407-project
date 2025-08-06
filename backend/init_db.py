from flask import Flask
from models import db
from config import Config

def init_db():
    # 创建 Flask 应用
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 导入所有模型以确保它们被注册
    from models.member import Member
    from models.booking import Booking
    from models.session import Session
    from models.membership import Membership
    from models.membership_type import MembershipType
    from models.payment import Payment
    
    try:
        # 在应用上下文中创建所有表
        with app.app_context():
            db.create_all()
            print("所有数据库表创建成功！")
            
    except Exception as e:
        print(f"创建表时出错：{str(e)}")
        raise

if __name__ == '__main__':
    init_db() 