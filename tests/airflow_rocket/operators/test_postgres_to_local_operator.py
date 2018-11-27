import json
import time
from collections import namedtuple
from os import path
from pathlib import Path

import docker
import pytest
from airflow.models import Connection

from airflow_rocket.operators.postgres_to_local_operator import (
    PostgresToLocalOperator,
    PostgresHook,
)


@pytest.fixture(scope="module")
def postgres_credentials():
    PostgresCredentials = namedtuple("PostgresCredentials", ["username", "password"])
    return PostgresCredentials("testuser", "testpass")


@pytest.fixture
def postgres(postgres_credentials):
    client = docker.from_env()
    container = client.containers.run(
        "postgres:10.5-alpine",
        environment={
            "POSTGRES_USER": postgres_credentials.username,
            "POSTGRES_PASSWORD": postgres_credentials.password,
        },
        ports={"5432/tcp": None},
        detach=True,
        volumes={
            path.join(path.dirname(__file__), "postgres-init.sql"): {
                "bind": "/docker-entrypoint-initdb.d/postgres-init.sql"
            }
        },
    )
    # do something better then sleep 10 here
    time.sleep(10)
    container.reload()
    return container


class TestPostgresToLocalOperator:
    def test_postgres_to_local_operator(
        self, test_dag, mocker, tmpdir, postgres, postgres_credentials
    ):
        output_path = str(tmpdir / "pg_dump")
        mocker.patch.object(
            PostgresHook,
            "get_connection",
            return_value=Connection(
                host="localhost",
                conn_type="postgres",
                login=postgres_credentials.username,
                password=postgres_credentials.password,
                port=postgres.attrs["NetworkSettings"]["Ports"]["5432/tcp"][0][
                    "HostPort"
                ],
            ),
        )

        task = PostgresToLocalOperator(
            task_id="test",
            postgres_conn_id="postgres",
            pg_query="SELECT * FROM dummy",
            local_path=output_path,
            dag=test_dag,
        )
        pytest.helpers.run_task(task=task, dag=test_dag)

        # Assert if output file exists
        output_file = Path(output_path)
        assert output_file.is_file()

        # Assert file contents
        expected = [
            {"id": 1, "name": "dummy1"},
            {"id": 2, "name": "dummy2"},
            {"id": 3, "name": "dummy3"},
        ]
        with open(output_file, "r") as f:
            assert json.load(f) == expected
