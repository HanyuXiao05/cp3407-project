# manage.py
from flask_migrate import Migrate
from app import create_app, db
from app.models import *  # 确保模型能被导入

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
