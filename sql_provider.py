"""
    Модуль для подставления параметров в sql запросы и получения их в виде строки.
"""
import os

from string import Template


class SQLProvider:
    """
        Класс для подставления параметров в запрос
    """
    def __init__(self, file_path: str) -> None:
        """
            Инициализация входными аргументами.

            Args:
                file_path: str. Строка с путем до директории с файлами с sql-запросами
        """
        self._scripts = {}

        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}', 'r').read())

    def get(self, name, **kwargs):
        """
            Выдает строку sql-запроса с подставленными параметрами.

            Args:
                name: str. Строка с названием файла
                kwargs. Параметры, которые надо подставить в запрос

            Returns:
                str. Запрос с подставленными параметрами.
        """
        return self._scripts[name].substitute(**kwargs)
