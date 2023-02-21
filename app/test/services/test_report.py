import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_get_report_service__returns_status_200__with_orders(client, create_orders, report_uri):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    response_json = response.json
    pytest.assume(response_json['most_requested_ingredient']['name'])
    pytest.assume(response_json['most_requested_ingredient']['num_requested'])
    pytest.assume(response_json['month_with_more_revenue']['month'])
    pytest.assume(response_json['best_customers']['customers'])
