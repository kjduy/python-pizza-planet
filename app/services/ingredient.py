from flask import Blueprint, request

from ..commands import (CreateCommand, GetAllCommand, GetByIdCommand,
                        UpdateCommand)
from ..common.http_methods import GET, POST, PUT
from ..receivers import IngredientReceiver
from .base import execute_command

ingredient = Blueprint("ingredient", __name__)


@ingredient.route("/", methods=GET)
def get_ingredients():
    response, status_code = execute_command(GetAllCommand, IngredientReceiver)
    return response, status_code


@ingredient.route("/id/<_id>", methods=GET)
def get_ingredient_by_id(_id: int):
    response, status_code = execute_command(GetByIdCommand, IngredientReceiver, _id)
    return response, status_code


@ingredient.route("/", methods=POST)
def create_ingredient():
    response, status_code = execute_command(
        CreateCommand, IngredientReceiver, request.json
    )
    return response, status_code


@ingredient.route("/", methods=PUT)
def update_ingredient():
    response, status_code = execute_command(
        UpdateCommand, IngredientReceiver, request.json
    )
    return response, status_code
