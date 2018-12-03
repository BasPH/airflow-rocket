"""Demo DAG showing BranchPythonOperator."""

import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="4_demo_branching",
    default_args=args,
    description="Demo DAG showing BranchPythonOperator.",
    schedule_interval="0 0 * * *",
)

# Definition of who is emailed on which weekday
weekday_person_to_email = {
    0: "Bob",  # Monday
    1: "Joe",  # Tuesday
    2: "Alice",  # Wednesday
    3: "Joe",  # Thursday
    4: "Alice",  # Friday
    5: "Alice",  # Saturday
    6: "Alice",  # Sunday
}


# Function returning name of task to execute
def _get_person_to_email(execution_date, **context):
    person = weekday_person_to_email[execution_date.weekday()]
    return f"email_{person.lower()}"


# Dummy task
create_report = DummyOperator(task_id="create_report", dag=dag)

# Branching task, the function above is passed to python_callable
branching = BranchPythonOperator(
    task_id="branching",
    python_callable=_get_person_to_email,
    provide_context=True,
    dag=dag,
)

# Execute branching task after create_report task
create_report >> branching

final_task = DummyOperator(
    task_id="final_task", trigger_rule=TriggerRule.ONE_SUCCESS, dag=dag
)

# Create dummy tasks for all people in the dict above,
# and execute all after the branching task
for name in set(weekday_person_to_email.values()):
    email_task = DummyOperator(task_id=f"email_{name.lower()}", dag=dag)
    branching >> email_task >> final_task
