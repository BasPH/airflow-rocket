"""Demo DAG showing airflow.utils.helpers.chain."""

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="7_demo_chain",
    default_args=args,
    description="Demo DAG showing airflow.utils.helpers.chain.",
    schedule_interval="0 0 * * *",
)

dummy_tasks = [DummyOperator(task_id=f"dummy_{i}", dag=dag) for i in range(5)]
airflow.utils.helpers.chain(*dummy_tasks)
