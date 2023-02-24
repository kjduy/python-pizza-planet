import pytest

from app.commands import CreateCommand, GetAllCommand, GetByIdCommand, UpdateCommand
from app.invoker import Invoker
from app.receivers import (
    BeverageReceiver,
    IngredientReceiver,
    OrderReceiver,
    SizeReceiver,
)
from app.receivers.base import BaseReceiver
from app.test.utils.functions import get_random_choice, shuffle_list


def __order(beverages: list, ingredients: list, size: dict, client_data: dict):
    beverages = list(map(lambda beverage: beverage.get("_id"), beverages))
    ingredients = list(map(lambda ingredient: ingredient.get("_id"), ingredients))
    size_id = size.get("_id")
    return {
        **client_data,
        "beverages": beverages,
        "ingredients": ingredients,
        "size_id": size_id,
    }


def __create_items(items: list, receiver: BaseReceiver):
    created_items = list(
        map(lambda item: Invoker(CreateCommand(receiver, item)).execute()[0], items)
    )
    return created_items


def __create_sizes_beverages_and_ingredients(
    beverages: list, ingredients: list, sizes: list
):
    created_beverages = __create_items(beverages, BeverageReceiver)
    created_ingredients = __create_items(ingredients, IngredientReceiver)
    created_sizes = __create_items(sizes, SizeReceiver)
    return (
        created_sizes if len(created_sizes) > 1 else created_sizes.pop(),
        created_beverages,
        created_ingredients,
    )


def test_get_all(app, beverages, ingredients, sizes, client_data):
    (
        created_sizes,
        created_beverages,
        created_ingredients,
    ) = __create_sizes_beverages_and_ingredients(beverages, ingredients, sizes)
    created_orders = []
    for _ in range(5):
        order = __order(
            shuffle_list(created_beverages)[:3],
            shuffle_list(created_ingredients)[:3],
            get_random_choice(created_sizes),
            client_data,
        )
        created_order, _ = OrderReceiver.create(order)
        created_orders.append(created_order)
    invoker = Invoker(GetAllCommand(OrderReceiver))
    orders_from_db, error = invoker.execute()
    searchable_orders = {db_order["_id"]: db_order for db_order in orders_from_db}
    pytest.assume(error is None)

    for created_order in created_orders:
        current_id = created_order["_id"]
        assert current_id in searchable_orders

        for param, value in created_order.items():
            pytest.assume(searchable_orders[current_id][param] == value)


def test_get_by_id(app, beverages, ingredients, size, client_data):
    (
        created_size,
        created_beverages,
        created_ingredients,
    ) = __create_sizes_beverages_and_ingredients(beverages, ingredients, [size])
    order = __order(created_beverages, created_ingredients, created_size, client_data)
    invoker_to_create = Invoker(CreateCommand(OrderReceiver, order))
    created_order, _ = invoker_to_create.execute()
    invoker_to_get_by_id = Invoker(GetByIdCommand(OrderReceiver, created_order["_id"]))
    order_from_db, error = invoker_to_get_by_id.execute()
    size_id = order.pop("size_id", None)
    ingredient_ids = order.pop("ingredients", [])
    beverage_ids = order.pop("beverages", [])
    pytest.assume(error is None)

    for param, value in created_order.items():
        pytest.assume(order_from_db[param] == value)
        pytest.assume(size_id == created_order["size"]["_id"])

        ingredients_in_detail = set(
            item["ingredient"]["_id"] for item in created_order["detail"]
        )
        beverages_in_detail = set(
            item["beverage"]["_id"] for item in created_order["detail"]
        )
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))
        pytest.assume(not beverages_in_detail.difference(beverage_ids))


def test_create(app, beverages, ingredients, size, client_data):
    (
        created_size,
        created_beverages,
        created_ingredients,
    ) = __create_sizes_beverages_and_ingredients(beverages, ingredients, [size])
    order = __order(created_beverages, created_ingredients, created_size, client_data)
    invoker = Invoker(CreateCommand(OrderReceiver, order))
    created_order, error = invoker.execute()
    size_id = order.pop("size_id", None)
    ingredient_ids = order.pop("ingredients", [])
    beverage_ids = order.pop("beverages", [])
    pytest.assume(error is None)

    for param, value in order.items():
        pytest.assume(param in created_order)
        pytest.assume(value == created_order[param])
        pytest.assume(created_order["_id"])
        pytest.assume(size_id == created_order["size"]["_id"])

        ingredients_in_detail = set(
            item["ingredient"]["_id"] for item in created_order["detail"]
        )
        beverages_in_detail = set(
            item["beverage"]["_id"] for item in created_order["detail"]
        )
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))
        pytest.assume(not beverages_in_detail.difference(beverage_ids))


def test_calculate_order_price(app, beverages, ingredients, size, client_data):
    (
        created_size,
        created_beverages,
        created_ingredients,
    ) = __create_sizes_beverages_and_ingredients(beverages, ingredients, [size])
    order = __order(created_beverages, created_ingredients, created_size, client_data)
    invoker = Invoker(CreateCommand(OrderReceiver, order))
    created_order, _ = invoker.execute()
    pytest.assume(
        created_order["total_price"]
        == round(
            created_size["price"]
            + sum(map(lambda beverage: beverage["price"], created_beverages))
            + sum(map(lambda ingredient: ingredient["price"], created_ingredients)),
            2,
        )
    )
