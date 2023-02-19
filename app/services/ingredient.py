from flask import Blueprint, jsonify, request

from ..commands import GetAllCommand, GetByIdCommand, CreateCommand, UpdateCommand
from ..common.http_methods import GET, POST, PUT
from ..invoker import Invoker
from ..receivers import IngredientReceiver

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=GET)
def get_ingredients():
    invoker = Invoker(GetAllCommand(IngredientReceiver))
    ingredients, error = invoker.execute()
    response = ingredients if not error else {'error': error}
    status_code = 200 if ingredients else 404 if not error else 400
    return jsonify(response), status_code


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    invoker = Invoker(GetByIdCommand(IngredientReceiver, _id))
    ingredient, error = invoker.execute()
    response = ingredient if not error else {'error': error}
    status_code = 200 if ingredient else 404 if not error else 400
    return jsonify(response), status_code


@ingredient.route('/', methods=POST)
def create_ingredient():
    invoker = Invoker(CreateCommand(IngredientReceiver, request.json))
    ingredient, error = invoker.execute()
    response = ingredient if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code


@ingredient.route('/', methods=PUT)
def update_ingredient():
    invoker = Invoker(UpdateCommand(IngredientReceiver, request.json))
    ingredient, error = invoker.execute()
    response = ingredient if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code
