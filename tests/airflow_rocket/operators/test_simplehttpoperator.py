"""
Airflow Connection mock example for blog post:
TBD
"""

from datetime import datetime

import pytest
from airflow.hooks.base_hook import BaseHook
from airflow.models import Connection
from airflow.operators.http_operator import SimpleHttpOperator


def test_simple_http_operator(test_dag, mocker):
    """Example test for SimpleHttpOperator"""

    mocker.patch.object(
        BaseHook,
        "get_connection",
        return_value=Connection(schema="https", host="api.sunrise-sunset.org"),
    )

    def _check_light(sunset_sunrise_response):
        import pdb
        pdb.set_trace()
        results = sunset_sunrise_response.json()["results"]

        # Example: 2019-02-20T06:59:30+00:00
        # Note: there is NO strftime format for +00:00! API docs say the timezone is
        # always UTC, i.e. +00:00, so considered simplest solution to remove and not use
        # 3rd party library. Python 3.7 can also do datetime.datetime.fromisoformat().
        sunrise = datetime.strptime(results["sunrise"][:-6], "%Y-%m-%dT%H:%M:%S")
        sunset = datetime.strptime(results["sunset"][:-6], "%Y-%m-%dT%H:%M:%S")

        if sunrise < datetime.utcnow() < sunset:
            print("It is light!")
        else:
            print("It is dark!")

        return True

    is_it_light = SimpleHttpOperator(
        task_id="is_it_light",
        http_conn_id="my_http_conn",
        endpoint="json",
        method="GET",
        data={"lat": "52.370216", "lng": "4.895168", "formatted": "0"},
        response_check=_check_light,
        dag=test_dag,
    )

    pytest.helpers.run_task(task=is_it_light, dag=test_dag)
