import pytest
from airflow.operators.bash_operator import BashOperator


class TestDummy:
    def test_dummy(self, test_dag, tmpdir):
        tmpfile = tmpdir.join("hello.txt")

        task = BashOperator(
            task_id="test", bash_command=f"echo 'hello' > {tmpfile}", dag=test_dag
        )
        pytest.helpers.run_task(task=task, dag=test_dag)

        assert len(tmpdir.listdir()) == 1
        assert tmpfile.read().replace("\n", "") == "hello"
