"""
    Модуль для выполнения запросов к бд.
"""

import os

from flask import Blueprint, render_template, request, current_app

from sql_provider import SQLProvider
from database import work_with_db
from access import login_permission_required

storage_app = Blueprint('storage_app', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@storage_app.route('/')
@login_permission_required
def storage_hello():
    """
        Вывод страницы главного меню запросов.
        
        Returns:
            Вызов страницы главного меню запросов.
    """
    return render_template('storage_hello.html')


@storage_app.route('/provider_contract_date', methods=['GET', 'POST'])
@login_permission_required
def provider_contract_date():
    """
        Вывод всех сведений о поставщиках, заключивших договора в заданный месяц и год.
        
        Returns:
           Вызов страницы для ввода параметров и страницы с результатами запроса.
    """
    if request.method == 'GET':
        return render_template('month_year.html')
    else:
        month_c = request.form.get('month_c', None)
        year_c = request.form.get('year_c', None)
        if (month_c and year_c) is not None:
            sql = provider.get('provider_contract_date.sql',
                               month_c=month_c, year_c=year_c)
            result = work_with_db(current_app.config['CONNECT_DB'], sql)
            if not result:
                return render_template('case_not_found.html')
            return render_template('output_table.html',
                                   header=f'Все сведения о поставщиках, '
                                          f'заключивших договора в {month_c}.{year_c}',
                                   items=['Фамилия', 'Город', 'Телефон',
                                          'Номер контракта',
                                          'Дата заключения контракта'],
                                   dictionaries=result)
        else:
            'Не выбран месяц или год'


@storage_app.route('/provider_contract_last', methods=['GET', 'POST'])
@login_permission_required
def provider_contract_last():
    """
        Вывод всех сведений о поставщиках, заключивших договора до заданного 
        количества дней назад.
        
        Returns:
           Вызов страницы для ввода параметров и страницы с результатами запроса.
    """
    if request.method == 'GET':
        return render_template('last_days.html')
    else:
        days_num = request.form.get('days_num', None)
        if days_num is not None:
            sql = provider.get('provider_contract_last.sql', days_num=days_num)
            result = work_with_db(current_app.config['CONNECT_DB'], sql)
            if not result:
                return render_template('case_not_found.html')
            return render_template('output_table.html',
                                   header=f'Все сведения о поставщиках, '
                                          f'заключивших договора за '
                                          f'последние {days_num} дней',
                                   items=['Фамилия', 'Город', 'Телефон',
                                          'Номер контракта',
                                          'Дата заключения контракта'],
                                   dictionaries=result)
        else:
            'Не выбраны дни'


@storage_app.route('/supply_date', methods=['GET', 'POST'])
@login_permission_required
def supply_date():
    """
        Вывод всех поставок за заданную дату.
        
        Returns:
           Вызов страницы для ввода параметров и страницы с результатами запроса.           
    """
    if request.method == 'GET':
        return render_template('supply_date.html')
    else:
        prefix = request.form.get('prefix', None)
        if prefix is not None:
            sql = provider.get('supply_date.sql', supply_date=prefix)
            result = work_with_db(current_app.config['CONNECT_DB'], sql)
            if not result:
                return render_template('case_not_found.html')
            return render_template('output_table.html',
                                   header=f'Все поставки, в заданную дату: '
                                          f' {prefix}',
                                   items=['Номер поставки', 'Дата',
                                          'Стоимость поставки', 'Количество товаров'],
                                   dictionaries=result)
        else:
            'Не выбран префикс'
