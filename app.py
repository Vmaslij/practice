"""
    Главный модуль, используемый при запуске приложения, при попадании на главную страницу.
"""

import json

from flask import Flask, render_template, session

from scenario_storage.routes import storage_app
from scenario_auth.routes import auth_app
from scenario_basket.routes import basket_app
from access import login_permission_required

app = Flask(__name__)

app.register_blueprint(storage_app, url_prefix='/storage')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(basket_app, url_prefix='/basket')

app.config['SECRET_KEY'] = 'bd'

app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))

with open("configs/file.json", "r") as f:
    db_config = json.load(f)

app.config['CONNECT_DB'] = db_config

with open("configs/config_for_read.json", "r") as f:
    config_read = json.load(f)

app.config['CONNECT_READ'] = db_config


@app.route('/')
@login_permission_required
def index():
    """
        Вызов страницы главного меню. 
    """
    return render_template('main_menu.html')


@app.route('/exit_page')
@login_permission_required
def exit_page():
    """
        Очистить сессию и вызвать страницу выхода. 
    """
    session.clear()
    return render_template('exit_page.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
