from flask import Blueprint, jsonify, request

from ..commands import CreateCommand, GetAllCommand, GetByIdCommand, UpdateCommand
from ..common.http_methods import GET, POST, PUT
from ..receivers import SizeReceiver
from .base import execute_command

size = Blueprint("size", __name__)


@size.route("/", methods=GET)
def get_sizes():
    response, status_code = execute_command(GetAllCommand, SizeReceiver)
    return response, status_code


@size.route("/id/<_id>", methods=GET)
def get_size_by_id(_id: int):
    response, status_code = execute_command(GetByIdCommand, SizeReceiver, _id)
    return response, status_code


@size.route("/", methods=POST)
def create_size():
    response, status_code = execute_command(CreateCommand, SizeReceiver, request.json)
    return response, status_code


@size.route("/", methods=PUT)
def update_size():
    response, status_code = execute_command(UpdateCommand, SizeReceiver, request.json)
    return response, status_code
