from pyexpat import model
from flask import Flask
from flask_admin import Admin
from app.admin  import AdminView


from app.settings import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__ , static_folder="static" , static_url_path="/static/")
app.config.from_object(Config)
db = SQLAlchemy(app)


migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

from app import routes, models, errors


admin = Admin(app, name='Dashboard')
admin.add_view(AdminView(models.User, db.session))
admin.add_view(AdminView(models.Recipe, db.session))
