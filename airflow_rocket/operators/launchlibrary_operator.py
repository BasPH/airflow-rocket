"""
Airflow operator for handling the Launch Library API.
https://launchlibrary.net/1.4
"""

import json
import pathlib
import posixpath
from typing import Optional

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from airflow_rocket.hooks.launchlibrary_hook import LaunchLibraryHook


class LaunchLibraryOperator(BaseOperator):
    """
    Airflow operator querying the Launch Library API
    and writing the result to file.
    """

    ui_color = "#101010"
    ui_fgcolor = "#FFF"
    template_fields = ("_result_path", "_result_filename", "_params")

    @apply_defaults
    def __init__(
        self,
        result_path: str = "/data/launchlibrary/ds={{ ds }}",
        result_filename: str = "launches.json",
        endpoint: str = "launch",
        params: Optional[dict] = None,
        conn_id: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._result_path = result_path
        self._result_filename = result_filename
        self._endpoint = endpoint
        self._params = params
        self._conn_id = conn_id

    def execute(self, context):
        self.log.info("Fetching Launch Library data.")

        hook = LaunchLibraryHook(conn_id=self._conn_id)
        response = hook.get(endpoint=self._endpoint, params=self._params)

        pathlib.Path(self._result_path).mkdir(parents=True, exist_ok=True)
        with open(posixpath.join(self._result_path, self._result_filename), "w") as f:
            f.write(json.dumps(response, indent=4))
            self.log.info(f"Wrote result to {f.name}")
