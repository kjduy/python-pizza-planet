from flask import Blueprint, jsonify, request

from ..commands import GetReportCommand
from ..common.http_methods import GET
from ..receivers import ReportReceiver
from .base import execute_command

report = Blueprint("report", __name__)


@report.route("/", methods=GET)
def get_report():
    response, status_code = execute_command(GetReportCommand, ReportReceiver)
    return response, status_code
