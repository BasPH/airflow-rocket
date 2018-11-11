"""This DAG downloads daily rocket launches from Launch Library."""

# pylint: disable=ungrouped-imports
import json
import pathlib
import posixpath

import airflow
import requests
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

# pylint: enable=ungrouped-imports

args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(10)}

dag = DAG(
    dag_id="download_rocket_launches",
    default_args=args,
    description="DAG downloading rocket launches from Launch Library.",
    schedule_interval="0 0 * * *",
)


def _download_rocket_launches(ds, tomorrow_ds, **context):
    query = f"https://launchlibrary.net/1.4/launch?startdate={ds}&enddate={tomorrow_ds}"

    result_path = f"/data/rocket_launches/ds={ds}"
    pathlib.Path(result_path).mkdir(parents=True, exist_ok=True)

    response = requests.get(query)
    with open(posixpath.join(result_path, "launches.json"), "w") as f:
        f.write(response.text)


def _print_stats(ds, **context):
    with open(f"/data/rocket_launches/ds={ds}/launches.json") as f:
        data = json.load(f)
        rockets_launched = [launch["name"] for launch in data["launches"]]
        rockets_str = ""
        if rockets_launched:
            rockets_str = f" ({' & '.join(rockets_launched)})"

        print(f"{len(rockets_launched)} rocket launch(es) on {ds}{rockets_str}.")


download_rocket_launches = PythonOperator(
    task_id="download_rocket_launches",
    python_callable=_download_rocket_launches,
    provide_context=True,
    dag=dag,
)
print_stats = PythonOperator(
    task_id="print_stats", python_callable=_print_stats, provide_context=True, dag=dag
)

download_rocket_launches >> print_stats
