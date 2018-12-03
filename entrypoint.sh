#!/usr/bin/env bash

# This check is to verify if the current directory contains a .airflow-rocket file.
# If not (when somebody mounts his/her own dags volume), the Airflow DB is initialised
# to get a fresh install of all DAGs.
if [ ! -f /root/airflow/dags/.airflow-rocket ]; then
    airflow initdb
fi

airflow scheduler &
airflow webserver
