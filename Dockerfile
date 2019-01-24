FROM continuumio/miniconda3:4.5.11

ENV SLUGIFY_USES_TEXT_UNIDECODE=yes \
	PYTHONDONTWRITEBYTECODE=1 \
	AIRFLOW__CORE__LOAD_EXAMPLES=False \
	AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True

RUN mkdir -p /root/airflow_rocket/src
COPY environment.yml /root/airflow_rocket
COPY setup.py /root/airflow_rocket
COPY entrypoint.sh /root/airflow_rocket
COPY src /root/airflow_rocket/src
COPY dags /root/airflow/dags

# hadolint ignore=DL3008,DL3013
RUN apt-get update && \
	apt-get install -y gcc g++ --no-install-recommends && \
    conda env update -f /root/airflow_rocket/environment.yml -n base && \
    pip install /root/airflow_rocket && \
    airflow initdb && \
	apt-get remove -y --purge gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# ENV AIRFLOW__SCHEDULER__MAX_THREADS=1
# ENV AIRFLOW__WEBSERVER__WORKER_REFRESH_INTERVAL=0
# ENV AIRFLOW__WEBSERVER__WORKERS=1

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "/root/airflow_rocket/entrypoint.sh"]
