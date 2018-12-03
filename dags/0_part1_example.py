"""DAG shown in part 1 of Airflow blog post."""

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="0_part1_example",
    default_args=args,
    description="DAG shown in part 1 of Airflow blog post.",
    schedule_interval="0 0 * * *",
)

tasks = {i: DummyOperator(task_id=f"task{i}", dag=dag) for i in range(1, 10)}

tasks[1] >> [tasks[2], tasks[3]]
tasks[2] >> tasks[4] >> [tasks[5], tasks[7]] >> tasks[9]
tasks[3] >> tasks[6] >> tasks[7]
tasks[5] >> tasks[7] >> tasks[8] >> tasks[9]
