from flask import Blueprint, jsonify, request

from ..commands import GetReportCommand
from ..common.http_methods import GET
from ..invoker import Invoker
from ..receivers import ReportReceiver

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    invoker = Invoker(GetReportCommand(ReportReceiver))
    report, error = invoker.execute()
    response = report if not error else {'error': error}
    status_code = 200 if report else 404 if not error else 400
    return jsonify(response), status_code