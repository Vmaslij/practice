"""
    Модуль работы с корзиной (главный бизнес-процесс).
"""
import os

from datetime import date
from flask import Blueprint, render_template, session, request, current_app, redirect

from database import work_with_db, db_update
from sql_provider import SQLProvider
from access import login_permission_required
from .utils import add_to_basket, clear_basket, sum_by_key

basket_app = Blueprint('basket_app', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@basket_app.route('/', methods=['GET', 'POST'])
@login_permission_required
def order_list_handler():
    """
        Отображает на страницу список товаров и список товаров,
        добавленных в корзину.

    Returns:
        Вызывает страницу со списком товаров и корзиной.
    """
    db_config = current_app.config['CONNECT_DB']
    if request.method == 'GET':
        current_basket = session.get('basket', [])
        sql = provider.get('order_list.sql')
        items = work_with_db(db_config, sql)
        return render_template('basket_order_list.html',
                               items=items,
                               basket=current_basket)
    else:
        item_id = request.form['id_pr']
        sql = provider.get('order_item.sql', item_id=item_id)
        items = work_with_db(db_config, sql)
        if not items:
            return 'Item not found'
        if request.form.get('delete', None) == "Убрать":
            add_to_basket(items, -1)
        else:
            add_to_basket(items, 1)
        return redirect('/basket')


@basket_app.route('/buy')
@login_permission_required
def buy_basket_handler():
    """
        Создает новую поставку в таблице поставок и заносит во
        вспомогательную таблицу список купленных товаров.

        Returns:
            Перенаправляет на страницу очистки корзины.
    """
    basket = session.get('basket', [])
    db_config = current_app.config['CONNECT_DB']
    if basket:
        supply_date = date.today()
        sum_price = sum_by_key('price_product')
        sum_amount = sum_by_key('pr_amount')
        sql = provider.get('insert_bas.sql',
                           date_supply=str(supply_date),
                           price_supply=sum_price,
                           amount_supply=sum_amount)
        response = db_update(db_config, sql)
        supply_id = work_with_db(db_config,
                                 provider.get('last_supply_id.sql'))[0]['sup_id']
        for item in basket:
            item_id = item.get('product_id')
            amount = item.get('pr_amount')
            sql = provider.get('buy_product.sql',
                               id_supply=supply_id,
                               id_product=item_id,
                               amount_product=amount)
            response = db_update(db_config, sql)
            clear_basket()
        return render_template('basket_sold.html')
    return redirect('clear')


@basket_app.route('/clear')
@login_permission_required
def clear_basket_handler():
    """
        Чистит корзину.

        Returns:
        Вызывает страницу со списком товаров и пустой корзиной.
    """
    clear_basket()
    return redirect('/basket')
