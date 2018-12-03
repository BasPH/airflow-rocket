"""Demo DAG initialising BaseHook in function to avoid Airflow DB calls."""

# pylint: disable=ungrouped-imports
import airflow
import requests
from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="9_basehook_get_connection",
    default_args=args,
    schedule_interval="@daily",
    description="Demo DAG initialising BaseHook in function to avoid Airflow DB calls.",
)


def _call_http():
    host = BaseHook.get_connection("http_default").host
    response = requests.get(host)
    print(response.text)


call_http = PythonOperator(task_id="call_http", python_callable=_call_http, dag=dag)
