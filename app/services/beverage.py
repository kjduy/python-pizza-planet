from flask import Blueprint, request

from ..commands import (CreateCommand, GetAllCommand, GetByIdCommand,
                        UpdateCommand)
from ..common.http_methods import GET, POST, PUT
from ..receivers import BeverageReceiver
from .base import execute_command

beverage = Blueprint("beverage", __name__)


@beverage.route("/", methods=GET)
def get_beverages():
    response, status_code = execute_command(GetAllCommand, BeverageReceiver)
    return response, status_code


@beverage.route("/id/<_id>", methods=GET)
def get_beverage_by_id(_id: int):
    response, status_code = execute_command(GetByIdCommand, BeverageReceiver, _id)
    return response, status_code


@beverage.route("/", methods=POST)
def create_beverage():
    response, status_code = execute_command(
        CreateCommand, BeverageReceiver, request.json
    )
    return response, status_code


@beverage.route("/", methods=PUT)
def update_beverage():
    response, status_code = execute_command(
        UpdateCommand, BeverageReceiver, request.json
    )
    return response, status_code
