"""This DAG demonstrates the PythonSensor."""
from datetime import datetime

import airflow
from airflow import DAG
from airflow.contrib.sensors.python_sensor import PythonSensor
from airflow.operators.bash_operator import BashOperator

default_args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="bring_me_coffee",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    description="Example PythonSensor",
)


def _time_for_coffee():
    if 6 <= datetime.now().hour < 12:
        return True
    else:
        return False


time_for_coffee = PythonSensor(
    task_id="time_for_coffee",
    python_callable=_time_for_coffee,
    mode="reschedule",
    dag=dag,
)

make_coffee = BashOperator(
    task_id="make_coffee", bash_command="echo 'Time for coffee!'", dag=dag
)

time_for_coffee >> make_coffee
