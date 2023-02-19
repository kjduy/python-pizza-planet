from flask import Blueprint, jsonify, request

from ..commands import GetAllCommand, GetByIdCommand, CreateCommand, UpdateCommand
from ..common.http_methods import GET, POST, PUT
from ..invoker import Invoker
from ..receivers import BeverageReceiver

beverage = Blueprint('beverage', __name__)


@beverage.route('/', methods=GET)
def get_beverages():
    invoker = Invoker(GetAllCommand(BeverageReceiver))
    beverages, error = invoker.execute()
    response = beverages if not error else {'error': error}
    status_code = 200 if beverages else 404 if not error else 400
    return jsonify(response), status_code


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    invoker = Invoker(GetByIdCommand(BeverageReceiver, _id))
    beverage, error = invoker.execute()
    response = beverage if not error else {'error': error}
    status_code = 200 if beverage else 404 if not error else 400
    return jsonify(response), status_code


@beverage.route('/', methods=POST)
def create_beverage():
    invoker = Invoker(CreateCommand(BeverageReceiver, request.json))
    beverage, error = invoker.execute()
    response = beverage if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code


@beverage.route('/', methods=PUT)
def update_beverage():
    invoker = Invoker(UpdateCommand(BeverageReceiver, request.json))
    beverage, error = invoker.execute()
    response = beverage if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code
