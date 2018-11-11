#!/usr/bin/env bash

if [ ! -f /root/airflow/dags/.airflow-rocket ]; then
    airflow initdb
fi

airflow scheduler &
airflow webserver
