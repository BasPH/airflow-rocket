"""This DAG demonstrates the BashOperator with templates files."""

from os import path

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="a_templated_bashoperator",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    description="BashOperator with templated file.",
    template_searchpath=path.join(path.dirname(__file__), "templates"),
)

BashOperator(
    task_id="run_templated_bashoperator",
    bash_command="a_templated_bashoperator/run_this.sh",
    dag=dag,
)
