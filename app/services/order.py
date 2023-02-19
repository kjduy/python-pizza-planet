from flask import Blueprint, jsonify, request

from ..commands import GetAllCommand, GetByIdCommand, CreateCommand
from ..common.http_methods import GET, POST
from ..invoker import Invoker
from ..receivers import OrderReceiver

order = Blueprint('order', __name__)


@order.route('/', methods=GET)
def get_orders():
    invoker = Invoker(GetAllCommand(OrderReceiver))
    orders, error = invoker.execute()
    response = orders if not error else {'error': error}
    status_code = 200 if orders else 404 if not error else 400
    return jsonify(response), status_code


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    invoker = Invoker(GetByIdCommand(OrderReceiver, _id))
    order, error = invoker.execute()
    response = order if not error else {'error': error}
    status_code = 200 if order else 404 if not error else 400
    return jsonify(response), status_code


@order.route('/', methods=POST)
def create_order():
    invoker = Invoker(CreateCommand(OrderReceiver, request.json))
    order, error = invoker.execute()
    response = order if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code
