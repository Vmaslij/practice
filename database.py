"""
    Модуль для подключения к базе данных и выполнения запросов к ней.
"""

from pymysql import connect
from pymysql.err import OperationalError


class DBConnection:
    """
        Класс для подключения к базе данных
    """

    def __init__(self, config: dict) -> None:
        """
            Инициализация входными аргументами.

            Args:
                config: dict. Словарь для подключения к бд с ключами:
                  "host": Имя хоста
                  "port": Порт сервера
                  "user": Имя пользователя
                  "password": Пароль пользователя
                  "db": Название схемы в бд
        """
        self.config = config

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print("Неверный логин или пароль.")
                return None
            if err.args[0] == 1049:
                print("Такой базы данных не существует.")
                return None
            if err.args[0] == 2003:
                print("Неверно введен порт/хост для подключения к серверу.")
                return None
        except UnicodeEncodeError as err:
            print("Были введены символы на русском языке.")
            return None

    def __exit__(self, exc_type, exc_value, exc_trace) -> bool:
        if exc_value:
            print(exc_value.args)
            if exc_value.args[0] == 'Курсор не был создан':
                print('Курсор не был создан')
            elif exc_value.args[0] == 1064:
                print("Синтаксическая ошибка в запросе.")
            elif exc_value.args[0] == 1146:
                print("Такой таблицы не существует.")
            elif exc_value.args[0] == 1054:
                print("Такого столбца не существует.")
        else:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        return True


def work_with_db(config: dict, sql: str) -> list:
    """
        Возвращает результат sql-запроса в виде списка.

        Args:
            config: dict. Словарь для подключения к бд
            sql: str. Строка с sql-запросом

        Returns:
            list. Результат запроса в виде списка.
    """
    result = []
    with DBConnection(config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не был создан')
        elif cursor:
            cursor.execute(sql)
            schema = [column[0] for column in cursor.description]
            result = []
            for str in cursor.fetchall():
                result.append(dict(zip(schema, str)))
        return result


def db_update(config: dict, _sql: str):
    """
        Выполняет запросы insert, update, delete.

        Args:
            config: dict. Словарь для подключения к бд
            _sql: str. Строка с sql-запросом
        Returns:
            None
    """
    with DBConnection(config) as cursor:
        if cursor is None:
            raise ValueError('Курсор None')
        elif cursor:
            cursor.execute(_sql)
