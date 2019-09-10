#  Created by Marcello Monachesi at 9/6/19, 5:30 PM

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

admin = Admin(app, name='Security Camera System', template_mode='bootstrap3')

from app.models import IPCamera

admin.add_view(ModelView(IPCamera, db.session))

from app import routes, models, errors
