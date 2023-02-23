import pytest

from app.commands import (CreateCommand, GetAllCommand, GetByIdCommand,
                          UpdateCommand)
from app.invoker import Invoker
from app.receivers import IngredientReceiver


def test_get_all(app, ingredients: list):
    created_ingredients = list(
        map(
            lambda ingredient: Invoker(
                CreateCommand(IngredientReceiver, ingredient)
            ).execute()[0],
            ingredients,
        )
    )
    invoker = Invoker(GetAllCommand(IngredientReceiver))
    ingredients_from_db, error = invoker.execute()
    searchable_ingredients = {
        db_ingredient["_id"]: db_ingredient for db_ingredient in ingredients_from_db
    }
    pytest.assume(error is None)

    for created_ingredient in created_ingredients:
        current_id = created_ingredient["_id"]
        assert current_id in searchable_ingredients

        for param, value in created_ingredient.items():
            pytest.assume(searchable_ingredients[current_id][param] == value)


def test_get_by_id(app, ingredient: dict):
    invoker_to_create = Invoker(CreateCommand(IngredientReceiver, ingredient))
    created_ingredient, _ = invoker_to_create.execute()
    invoker_to_get_by_id = Invoker(
        GetByIdCommand(IngredientReceiver, created_ingredient["_id"])
    )
    ingredient_from_db, error = invoker_to_get_by_id.execute()
    pytest.assume(error is None)

    for param, value in created_ingredient.items():
        pytest.assume(ingredient_from_db[param] == value)


def test_create(app, ingredient: dict):
    invoker = Invoker(CreateCommand(IngredientReceiver, ingredient))
    created_ingredient, error = invoker.execute()
    pytest.assume(error is None)

    for param, value in ingredient.items():
        pytest.assume(param in created_ingredient)
        pytest.assume(value == created_ingredient[param])
        pytest.assume(created_ingredient["_id"])


def test_update(app, ingredient: dict):
    invoker_to_create = Invoker(CreateCommand(IngredientReceiver, ingredient))
    created_ingredient, _ = invoker_to_create.execute()
    updated_fields = {"name": "updated", "price": 10}
    invoker_to_update = Invoker(
        UpdateCommand(
            IngredientReceiver, {"_id": created_ingredient["_id"], **updated_fields}
        )
    )
    updated_ingredient, error = invoker_to_update.execute()
    pytest.assume(error is None)

    invoker_to_get_by_id = Invoker(
        GetByIdCommand(IngredientReceiver, created_ingredient["_id"])
    )
    ingredient_from_db, error = invoker_to_get_by_id.execute()
    pytest.assume(error is None)

    for param, value in updated_fields.items():
        pytest.assume(updated_ingredient[param] == value)
        pytest.assume(ingredient_from_db[param] == value)
