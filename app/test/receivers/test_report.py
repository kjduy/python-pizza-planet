import pytest

from app.commands import GetReportCommand
from app.invoker import Invoker
from app.receivers import ReportReceiver


def test_get_report(app, create_orders):
    invoker = Invoker(GetReportCommand(ReportReceiver))
    report_from_db, error = invoker.execute()
    pytest.assume(error is None)
    pytest.assume(report_from_db['most_requested_ingredient']['name'])
    pytest.assume(report_from_db['most_requested_ingredient']['count'])
    pytest.assume(report_from_db['month_with_more_revenue']['month'])
    pytest.assume(report_from_db['best_customers']['customers'])
