#  Created by Marcello Monachesi at 9/6/19, 5:30 PM

from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')
