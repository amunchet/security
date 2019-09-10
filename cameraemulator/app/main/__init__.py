#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
