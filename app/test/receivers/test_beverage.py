import pytest

from app.commands import CreateCommand, UpdateCommand, GetByIdCommand, GetAllCommand
from app.invoker import Invoker
from app.receivers import BeverageReceiver


def test_get_all(app, beverages: list):
    created_beverages = list(map(lambda beverage: Invoker(CreateCommand(BeverageReceiver, beverage)).execute()[0], beverages))
    invoker = Invoker(GetAllCommand(BeverageReceiver))
    beverages_from_db, error = invoker.execute()
    searchable_beverages = {db_beverage['_id']: db_beverage for db_beverage in beverages_from_db}
    pytest.assume(error is None)

    for created_beverage in created_beverages:
        current_id = created_beverage['_id']
        assert current_id in searchable_beverages

        for param, value in created_beverage.items():
            pytest.assume(searchable_beverages[current_id][param] == value)


def test_get_by_id(app, beverage: dict):
    invoker_to_create = Invoker(CreateCommand(BeverageReceiver, beverage))
    created_beverage, _ = invoker_to_create.execute()
    invoker_to_get_by_id = Invoker(GetByIdCommand(BeverageReceiver, created_beverage['_id']))
    beverage_from_db, error = invoker_to_get_by_id.execute()
    pytest.assume(error is None)

    for param, value in created_beverage.items():
        pytest.assume(beverage_from_db[param] == value)


def test_create(app, beverage: dict):
    invoker = Invoker(CreateCommand(BeverageReceiver, beverage))
    created_beverage, error = invoker.execute()
    pytest.assume(error is None)

    for param, value in beverage.items():
        pytest.assume(param in created_beverage)
        pytest.assume(value == created_beverage[param])
        pytest.assume(created_beverage['_id'])


def test_update(app, beverage: dict):
    invoker_to_create = Invoker(CreateCommand(BeverageReceiver, beverage))
    created_beverage, _ = invoker_to_create.execute()
    updated_fields = {
        'name': 'updated',
        'price': 10
    }
    invoker_to_update = Invoker(UpdateCommand(BeverageReceiver, {'_id': created_beverage['_id'], **updated_fields}))
    updated_beverage, error = invoker_to_update.execute()
    pytest.assume(error is None)

    invoker_to_get_by_id = Invoker(GetByIdCommand(BeverageReceiver, created_beverage['_id']))
    beverage_from_db, error = invoker_to_get_by_id.execute()
    pytest.assume(error is None)

    for param, value in updated_fields.items():
        pytest.assume(updated_beverage[param] == value)
        pytest.assume(beverage_from_db[param] == value)
