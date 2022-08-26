"""
    Модуль для авторизации пользователя.
"""
import os

from flask import Blueprint, render_template, session, request, current_app

from database import work_with_db
from sql_provider import SQLProvider
from access import login_permission_required

auth_app = Blueprint('auth_app', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@auth_app.route('/', methods=['GET', 'POST'])
@login_permission_required
def login_page():
    """
        Функция для авторизации пользователя.

        Returns:
            Страница для авторизации, с выводом сообщения об успешной авторизации
            или неуспешной авторизации.
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('Login', None)
        password = request.form.get('Password', None)

    if (login and password) is not None:
        sql = provider.get('auth.sql', log=login, passw=password)
        result = work_with_db(current_app.config['CONNECT_DB'], sql)

        if result:
            session['group_name'] = result[0]['group']
            return render_template('authorised.html')
        else:
            return render_template('unauthorised.html')
