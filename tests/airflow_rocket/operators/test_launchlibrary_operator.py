"""Tests for LaunchLibraryOperator"""
import glob
import json

import pytest
from airflow.hooks.base_hook import BaseHook
from airflow.models import Connection

from airflow_rocket.hooks.launchlibrary_hook import LaunchLibraryHook
from airflow_rocket.operators.launchlibrary_operator import LaunchLibraryOperator


# pylint: disable=no-self-use,too-few-public-methods
class TestLaunchLibraryOperator:
    """Tests for LaunchLibraryOperator"""

    def test_launchlibrary_operator(self, test_dag, mocker, tmpdir):
        """Write and validate a result file with LaunchLibraryOperator"""
        mocker.patch.object(BaseHook, "get_connection", return_value=Connection())
        testdata = {"this": "is", "a": "test"}
        mocker.patch.object(LaunchLibraryHook, "get", return_value=testdata)

        task = LaunchLibraryOperator(
            task_id="test",
            conn_id="launchlibrary",
            endpoint="launch",
            params={"startdate": "{{ ds }}", "enddate": "{{ tomorrow_ds }}"},
            result_path=str(tmpdir) + "/rocket_launches/ds={{ ds }}",
            result_filename="launches.json",
            dag=test_dag,
        )
        pytest.helpers.run_task(task=task, dag=test_dag)

        # Assert if file exists
        files = glob.glob(str(tmpdir) + "/rocket_launches/ds=*/launches.json")
        assert len(files) == 1

        # Assert file contents
        with open(files[0]) as f:
            assert json.load(f) == testdata
