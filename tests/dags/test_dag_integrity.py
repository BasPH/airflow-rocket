"""Test the validity of all DAGs."""

from os import path

import pytest
from airflow import models as airflow_models
from airflow.utils.dag_processing import list_py_file_paths

DAG_BASE_DIR = path.join(path.dirname(__file__), "..", "..", "dags")
DAG_PATHS = list_py_file_paths(DAG_BASE_DIR)


@pytest.mark.parametrize("dag_path", DAG_PATHS)
def test_dag_integrity(dag_path):
    """Import DAG files and check for a valid DAG instance."""
    dag_name = path.basename(dag_path)
    module = _import_file(dag_name, dag_path)
    assert any(isinstance(var, airflow_models.DAG) for var in vars(module).values())


def _import_file(module_name, module_path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
