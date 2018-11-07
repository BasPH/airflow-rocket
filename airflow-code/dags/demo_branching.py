"""Demo DAG showing BranchPythonOperator."""

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="demo_branching",
    default_args=args,
    description="Demo DAG showing BranchPythonOperator.",
    schedule_interval="0 0 * * *",
)

weekday_person_to_email = {
    0: "Bob",  # Monday
    1: "Joe",  # Tuesday
    2: "Alice",  # Wednesday
    3: "Joe",  # Thursday
    4: "Alice",  # Friday
    5: "Alice",  # Saturday
    6: "Alice",  # Sunday
}


def _get_person_to_email(**context):
    person = weekday_person_to_email[context["execution_date"].weekday()]
    return f"email_{person.lower()}"


create_report = DummyOperator(task_id="create_report", dag=dag)

branching = BranchPythonOperator(
    task_id="branching",
    python_callable=_get_person_to_email,
    provide_context=True,
    dag=dag,
)

create_report >> branching

final_task = DummyOperator(
    task_id="final_task", trigger_rule=TriggerRule.ONE_SUCCESS, dag=dag
)

for name in set(weekday_person_to_email.values()):
    email_task = DummyOperator(task_id=f"email_{name.lower()}", dag=dag)
    branching >> email_task >> final_task
