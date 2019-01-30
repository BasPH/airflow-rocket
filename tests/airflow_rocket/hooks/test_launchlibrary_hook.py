"""Tests for LaunchLibraryHook"""

from airflow.hooks.base_hook import BaseHook
from airflow.models import Connection

from airflow_rocket.hooks.launchlibrary_hook import LaunchLibraryHook, requests


# pylint: disable=no-self-use,too-few-public-methods
class TestLaunchLibraryHook:
    """Tests for LaunchLibraryHook"""

    def test_get(self, mocker):
        """Test if correct URL is formed."""
        mocker.patch.object(
            BaseHook,
            "get_connection",
            return_value=Connection(host="launchlibrary.net", schema="https"),
        )

        hook = LaunchLibraryHook(conn_id="test")
        mock_get = mocker.patch.object(requests.Session, "get")
        hook.get(
            endpoint="launch", params={"startdate": "2018-01-01", "enddate": "2018-02-01"}
        )

        mock_get.assert_called_once_with(
            url="https://launchlibrary.net/1.4/launch",
            params={"startdate": "2018-01-01", "enddate": "2018-02-01"},
        )
