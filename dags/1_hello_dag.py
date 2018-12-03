"""Demo DAG showing a Hello World example."""

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="1_hello_dag",
    default_args=args,
    description="Demo DAG showing a hello world example.",
)

t1 = BashOperator(task_id="sleep_a_bit", bash_command="sleep 5", dag=dag)

t2 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

t1 >> t2
