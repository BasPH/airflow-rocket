"""DAG shown in part 1 of Airflow blog post."""

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="part1_example",
    default_args=args,
    description="DAG shown in part 1 of Airflow blog post.",
    schedule_interval="0 0 * * *",
)

task1 = DummyOperator(task_id="task1", dag=dag)
task2 = DummyOperator(task_id="task2", dag=dag)
task3 = DummyOperator(task_id="task3", dag=dag)
task4 = DummyOperator(task_id="task4", dag=dag)
task5 = DummyOperator(task_id="task5", dag=dag)
task6 = DummyOperator(task_id="task6", dag=dag)
task7 = DummyOperator(task_id="task7", dag=dag)
task8 = DummyOperator(task_id="task8", dag=dag)
task9 = DummyOperator(task_id="task9", dag=dag)

task1 >> [task2, task3]
task2 >> task4 >> [task5, task7] >> task9
task3 >> task6 >> task7
task5 >> task7 >> task8 >> task9
