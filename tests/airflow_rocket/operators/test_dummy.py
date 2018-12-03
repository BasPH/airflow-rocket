"""Dummy Airflow test showing usage of test_dag and run_task()."""

# pylint: disable=no-self-use
import pytest
from airflow.operators.bash_operator import BashOperator


class TestDummy:
    """Dummy Airflow tests."""

    def test_dummy(self, test_dag, tmpdir):
        """Test BashOperator writing file to local disk."""
        tmpfile = tmpdir.join("hello.txt")

        task = BashOperator(
            task_id="test", bash_command=f"echo 'hello' > {tmpfile}", dag=test_dag
        )
        pytest.helpers.run_task(task=task, dag=test_dag)

        assert len(tmpdir.listdir()) == 1
        assert tmpfile.read().replace("\n", "") == "hello"
