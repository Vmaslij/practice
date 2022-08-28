"""
    Модуль для проверки уровня доступа.
"""

from flask import session, request, current_app, render_template
from functools import wraps


def group_permission_validation(config: dict, sess: session) -> bool:
    """
    Проверяет есть ли право доступа.

    Args:
        config: dict. Данные из файла с названиями модулей к которым
         есть доступ у определенной группы пользователей
        sess: session. Сессия, в которой хранится группа пользователя
    Returns:
        bool. Имеет ли пользователь право доступа.
    """
    group = sess.get('group_name', 'unauthorized')
    target_app = "" if len(request.endpoint.split('.')) == 1 \
        else request.endpoint.split('.')[0]
    if group in config and target_app in config[group]:
        return True
    return False


def login_permission_required(f):
    """
    Декоратор, проверяющий, есть ли право доступа к странице или выдающий ошибку.

    Args:
        f: function. Функция, перед которой ставится декоратор

    Returns:
        function. Добавляет код с проверкой перед функцией.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        """
        Проверяет есть ли право доступа или выдает страницу с сообщением об
        отсутствии прав доступа.

        Args:
            args. Неименованные аргументы функции
            kwargs. Поименованные аргументы функции

        Returns:
            f. Функция, перед которой стоит декоратор или вызов страницы
            с сообщением об отсутствии прав доступа.
        """
        if group_permission_validation(current_app.config['ACCESS_CONFIG'], session):
            return f(*args, **kwargs)
        return render_template('access_denied.html')

    return wrapper
