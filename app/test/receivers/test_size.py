import pytest

from app.commands import CreateCommand, GetAllCommand, GetByIdCommand, UpdateCommand
from app.invoker import Invoker
from app.receivers import SizeReceiver


def test_get_all(app, sizes: list):
    created_sizes = list(
        map(lambda size: Invoker(CreateCommand(SizeReceiver, size)).execute()[0], sizes)
    )
    invoker = Invoker(GetAllCommand(SizeReceiver))
    sizes_from_db, error = invoker.execute()
    searchable_sizes = {db_size["_id"]: db_size for db_size in sizes_from_db}
    pytest.assume(error is None)

    for created_size in created_sizes:
        current_id = created_size["_id"]
        assert current_id in searchable_sizes

        for param, value in created_size.items():
            pytest.assume(searchable_sizes[current_id][param] == value)


def test_get_by_id(app, size: dict):
    invoker_to_create = Invoker(CreateCommand(SizeReceiver, size))
    created_size, _ = invoker_to_create.execute()
    invoker_to_get_by_id = Invoker(GetByIdCommand(SizeReceiver, created_size["_id"]))
    size_from_db, error = invoker_to_get_by_id.execute()
    pytest.assume(error is None)

    for param, value in created_size.items():
        pytest.assume(size_from_db[param] == value)


def test_create(app, size: dict):
    invoker = Invoker(CreateCommand(SizeReceiver, size))
    created_size, error = invoker.execute()
    pytest.assume(error is None)

    for param, value in size.items():
        pytest.assume(param in created_size)
        pytest.assume(value == created_size[param])
        pytest.assume(created_size["_id"])


def test_update(app, size: dict):
    invoker_to_create = Invoker(CreateCommand(SizeReceiver, size))
    created_size, _ = invoker_to_create.execute()
    updated_fields = {"name": "updated", "price": 10}
    invoker_to_update = Invoker(
        UpdateCommand(SizeReceiver, {"_id": created_size["_id"], **updated_fields})
    )
    updated_size, error = invoker_to_update.execute()
    pytest.assume(error is None)

    invoker_to_get_by_id = Invoker(GetByIdCommand(SizeReceiver, created_size["_id"]))
    size_from_db, error = invoker_to_get_by_id.execute()
    pytest.assume(error is None)

    for param, value in updated_fields.items():
        pytest.assume(updated_size[param] == value)
        pytest.assume(size_from_db[param] == value)
