import pytest

from ..utils.functions import (
    shuffle_list, get_random_sequence,
    get_random_string
)


def client_data_mock() -> dict:
    return {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence()
    }


def order_mock(create_beverages, create_ingredients, create_sizes) -> dict:
    beverages = list(map(lambda beverage: beverage.get('_id'), create_beverages))
    ingredients = list(map(lambda ingredient: ingredient.get('_id'), create_ingredients))
    sizes = list(map(lambda size: size.get('_id'), create_sizes))
    return {
        **client_data_mock(),
        'beverages': shuffle_list(beverages)[:5],
        'ingredients': shuffle_list(ingredients)[:5],
        'size_id': shuffle_list(sizes)[0]
    }


@pytest.fixture
def order_uri():
    return '/order/'


@pytest.fixture
def client_data():
    return client_data_mock()


@pytest.fixture
def order(create_beverages, create_ingredients, create_sizes) -> dict:
    return order_mock(create_beverages, create_ingredients, create_sizes)


@pytest.fixture
def create_order(client, order_uri, order) -> list:
    return client.post(order_uri, json=order)


@pytest.fixture
def create_orders(client, order_uri, order) -> list:
    orders = []
    for _ in range(10):
        new_order = client.post(order_uri, json=order)
        orders.append(new_order.json)
    return orders
