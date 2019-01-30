"""This DAG prints the Airflow context."""
from pprint import pprint

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="2_airflow_context",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    description="DAG printing the Airflow context and execution date.",
)


def _print_exec_date_v1(**context):
    """Print the task execution date, reading from context argument."""
    print(context["execution_date"])


def _print_exec_date_v2(execution_date, **context):
    """Print the task execution date."""
    print(execution_date)


def _print_context(**context):
    """Print the Airflow context."""
    pprint(context)


print_exec_date_v1 = PythonOperator(
    task_id="print_exec_date_v1",
    python_callable=_print_exec_date_v1,
    provide_context=True,
    dag=dag,
)

print_exec_date_v2 = PythonOperator(
    task_id="print_exec_date_v2",
    python_callable=_print_exec_date_v2,
    provide_context=True,
    dag=dag,
)

print_context = PythonOperator(
    task_id="print_context", python_callable=_print_context, provide_context=True, dag=dag
)
