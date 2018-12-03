"""This DAG downloads daily rocket launches from Launch Library."""

import json

import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

from airflow_rocket.operators.launchlibrary_operator import LaunchLibraryOperator

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(10)}

dag = DAG(
    dag_id="8_download_rocket_launches_custom_package",
    default_args=args,
    description="DAG downloading rocket launches from Launch Library using custom package.",
    schedule_interval="0 0 * * *",
)

download_rocket_launches = LaunchLibraryOperator(
    task_id="download_rocket_launches",
    conn_id="launchlibrary",
    endpoint="launch",
    params={"startdate": "{{ ds }}", "enddate": "{{ tomorrow_ds }}"},
    result_path="/data/rocket_launches/ds={{ ds }}",
    result_filename="launches.json",
    dag=dag,
)


def _print_stats(ds, **context):
    with open(f"/data/rocket_launches/ds={ds}/launches.json") as f:
        data = json.load(f)
        rockets_launched = [launch["name"] for launch in data["launches"]]
        rockets_str = ""
        if rockets_launched:
            rockets_str = f" ({' & '.join(rockets_launched)})"

        print(f"{len(rockets_launched)} rocket launch(es) on {ds}{rockets_str}.")


print_stats = PythonOperator(
    task_id="print_stats", python_callable=_print_stats, provide_context=True, dag=dag
)

download_rocket_launches >> print_stats
