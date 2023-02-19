from flask import Blueprint, jsonify, request

from ..commands import GetAllCommand, GetByIdCommand, CreateCommand, UpdateCommand
from ..common.http_methods import GET, POST, PUT
from ..invoker import Invoker
from ..receivers import SizeReceiver

size = Blueprint('size', __name__)


@size.route('/', methods=GET)
def get_sizes():
    invoker = Invoker(GetAllCommand(SizeReceiver))
    sizes, error = invoker.execute()
    response = sizes if not error else {'error': error}
    status_code = 200 if size else 404 if not error else 400
    return jsonify(response), status_code


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    invoker = Invoker(GetByIdCommand(SizeReceiver, _id))
    size, error = invoker.execute()
    response = size if not error else {'error': error}
    status_code = 200 if size else 404 if not error else 400
    return jsonify(response), status_code


@size.route('/', methods=POST)
def create_size():
    invoker = Invoker(CreateCommand(SizeReceiver, request.json))
    size, error = invoker.execute()
    response = size if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code


@size.route('/', methods=PUT)
def update_size():
    invoker = Invoker(UpdateCommand(SizeReceiver, request.json))
    size, error = invoker.execute()
    response = size if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code
