from flask import Blueprint, jsonify, request

from .base import execute_command
from ..commands import GetAllCommand, GetByIdCommand, CreateCommand
from ..common.http_methods import GET, POST
from ..receivers import OrderReceiver

order = Blueprint('order', __name__)


@order.route('/', methods=GET)
def get_orders():
    response, status_code = execute_command(GetAllCommand, OrderReceiver)
    return response, status_code


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    response, status_code = execute_command(GetByIdCommand, OrderReceiver, _id)
    return response, status_code


@order.route('/', methods=POST)
def create_order():
    response, status_code = execute_command(CreateCommand, OrderReceiver, request.json)
    return response, status_code
