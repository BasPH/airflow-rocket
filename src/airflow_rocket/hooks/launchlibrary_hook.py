"""
Hook for reading from the Launch Library API.
https://launchlibrary.net/1.4
"""

from typing import Optional

import requests
from airflow import AirflowException
from airflow.hooks.base_hook import BaseHook


class LaunchLibraryHook(BaseHook):
    """Airflow hook connecting to Launch Library API."""

    def __init__(self, conn_id: Optional[str] = None, api_version: str = "1.4"):
        """LaunchLibraryHook constructor."""
        super().__init__(source=None)
        self._conn_id = conn_id
        self._api_version = api_version

        self._conn = None
        self._base_url = "https://launchlibrary.net"

    def get_conn(self):
        """Initialise and cache session."""
        if self._conn is None:
            session = requests.Session()
            self._conn = session
            if self._conn_id:
                try:
                    conn = self.get_connection(self._conn_id)
                    self._base_url = (
                        f"{conn.schema + '://' if conn.schema else ''}{conn.host}"
                    )
                except AirflowException:
                    self.log.warning(
                        f"Connection '{self._conn_id}' not found, using defaults."
                    )

        return self._conn

    def get(
        self, endpoint: str = "launch", params: Optional[dict] = None, **kwargs
    ) -> dict:
        """
        Fetch a JSON response from the Launch Library API.
        :param str endpoint: Launch Library API endpoint.
        :param dict params: Optional parameters to pass with the URL.
        :return: JSON response.
        :rtype: dict
        """
        session = self.get_conn()
        full_url = (
            f"{self._base_url[:-1] if self._base_url.endswith('/') else self._base_url}"
            f"/{self._api_version}"
            f"/{endpoint}"
        )
        response = session.get(url=full_url, params=params, **kwargs)

        if response.status_code not in (200, 404):
            # Launch Library returns 404 if no rocket launched in given interval.
            response.raise_for_status()

        return response.json()
