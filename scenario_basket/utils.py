"""
    Вспомогательный модуль для добавления товаров в корзину в сессии.
"""

from flask import session


def sum_by_key(key):
    """
        Считает сумму элементов по переданному ключу.

        Args:
            key: str. Ключ в словаре

        Returns:
            int. Сумма элементов.
    """
    basket = session.get('basket', [])
    summ = 0
    for i in basket:
        summ += i[key]
    return summ


def check_item_in_basket(item, basket, amount):
    """
        Проверяет, есть ли такой товар в корзине и изменяет
        количество товаров.

        Args:
            item: dict. Словарь с параметрами товара
            basket: list. Список товаров в корзине
            amount: int. Количество товаров
        Returns:
            bool. Есть ли такой товар в корзине.
    """
    for i in range(len(basket)):
        if item['product_id'] == basket[i]['product_id']:
            basket[i]['pr_amount'] += amount
            if basket[i]['pr_amount'] == 0:
                basket.pop(i)
            return True
    return False


def add_to_basket(items, amount):
    """
        Добавление товаров из списка в корзину.

        Args:
            items: list. Список товаров для добавления в корзину
            amount: int. Количество товаров
        Returns:
            None.
    """
    basket = session.get('basket', [])
    for item in items:
        if not check_item_in_basket(item, basket, amount):
            item['pr_amount'] = 1
            basket.append(item)
    session['basket'] = basket


def clear_basket():
    """
        Очистить корзину.
    """
    if 'basket' in session:
        session.pop('basket')
