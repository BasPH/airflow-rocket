"""Tests for the Slack on_failure_callback function."""

# pylint: disable=redefined-outer-name,no-self-use,ungrouped-imports
import datetime
from unittest import mock

import airflow
import pytest
from airflow import DAG
from airflow.models import Connection
from airflow.operators.bash_operator import BashOperator

from airflow_rocket.utils.slack import send_slack_failure_message, BaseHook, requests


@pytest.fixture
def test_dag():
    """Dummy DAG with on_failure_callback configured."""
    return DAG(
        "test_slack",
        default_args={
            "owner": "airflow",
            "start_date": datetime.datetime(2018, 1, 1),
            "on_failure_callback": send_slack_failure_message,
        },
        schedule_interval=datetime.timedelta(days=1),
    )


class TestSlackCallback:
    """Tests for airflow_rocket.utils.slack."""

    def test_slack_callback(self, test_dag, mocker):
        """Test if expected call to requests.post is made."""
        fake_slack_url = "https://hooks.slack.com/test"
        mocker.patch.object(
            BaseHook, "get_connection", return_value=Connection(host=fake_slack_url)
        )
        mock_post = mocker.patch.object(requests, "post")

        failing_task = BashOperator(
            task_id="failure_test", bash_command="exit 123", dag=test_dag
        )

        with pytest.raises(airflow.exceptions.AirflowException):
            pytest.helpers.run_task(task=failing_task, dag=test_dag)

            assert mock_post.assert_called_once_with(
                fake_slack_url,
                data=mock.ANY,
                headers={"Content-type": "application/json"},
            )
