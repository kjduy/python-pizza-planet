from flask import jsonify

from ..invoker import Invoker


def execute_command(command, receiver, input_data=None):
    invoker = Invoker(
        command(receiver, input_data) if input_data else command(receiver)
    )
    entity, error = invoker.execute()
    response = entity if not error else {"error": error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code
