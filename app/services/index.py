from flask import Blueprint, jsonify

from ..commands import TestConnectionCommand
from ..common.http_methods import GET
from ..invoker import Invoker
from ..receivers import IndexReceiver

index = Blueprint("index", __name__)


@index.route("/", methods=GET)
def get_index():
    invoker = Invoker(TestConnectionCommand(IndexReceiver))
    is_database_up, error = invoker.execute()
    return jsonify(
        {
            "version": "0.0.2",
            "status": "up" if is_database_up else "down",
            "error": error,
        }
    )
