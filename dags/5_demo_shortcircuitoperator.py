"""Demo DAG showing ShortCircuitOperator."""

import datetime

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import ShortCircuitOperator
from dateutil.relativedelta import relativedelta

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="5_demo_shortcircuitoperator",
    default_args=args,
    description="Demo DAG showing ShortCircuitOperator.",
    schedule_interval="0 0 * * *",
)


def _check_date(execution_date, **context):
    return execution_date > (datetime.datetime.now() - relativedelta(weeks=1))


check_date = ShortCircuitOperator(
    task_id="check_if_min_date",
    python_callable=_check_date,
    provide_context=True,
    dag=dag,
)

task1 = DummyOperator(task_id="task1", dag=dag)
task2 = DummyOperator(task_id="task2", dag=dag)

check_date >> task1 >> task2
