"""Functions for sending messages to Slack."""

import json
import sys

import requests
from airflow.hooks.base_hook import BaseHook


def send_slack_failure_message(context):
    """
    Send a failure message to Slack.
    :param context: Airflow context.
    """
    connection = BaseHook.get_connection("slack")
    data = {"text": _format_message(context)}
    headers = {"Content-type": "application/json"}
    requests.post(connection.host, data=json.dumps(data), headers=headers)


def _format_message(context):
    task_instance = context["task_instance"]
    exctype, excvalue = sys.exc_info()[:2]

    text = (
        ":skull_and_crossbones: *Airflow task failed*.\n"
        f"Task instance {str(task_instance)} \n"
        f"Try {task_instance.try_number} out of {task_instance.max_tries + 1} \n"
        f"Exception {exctype} : {excvalue}! \n"
        f"Log: {task_instance.log_url} \n"
        f"Host: {task_instance.hostname}\n"
        f"Log file: {task_instance.log_filepath} \n"
    )
    return text
