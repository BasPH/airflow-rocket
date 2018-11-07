FROM continuumio/miniconda3:4.5.11

ENV SLUGIFY_USES_TEXT_UNIDECODE=yes \
	PYTHONDONTWRITEBYTECODE=1 \
	AIRFLOW__CORE__LOAD_EXAMPLES=False \
	AIRFLOW__WEBSERVER__EXPOSE_CONFIG=True

COPY environment.yml /tmp/environment.yml

RUN apt-get update && \
	apt-get install -y gcc g++ --no-install-recommends && \
    conda env update -f /tmp/environment.yml -n base && \
	airflow initdb && \
	apt-get remove -y --purge gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean -y

COPY airflow-code/dags /root/airflow/dags

# ENV AIRFLOW__SCHEDULER__MAX_THREADS=1
# ENV AIRFLOW__WEBSERVER__WORKER_REFRESH_INTERVAL=0
# ENV AIRFLOW__WEBSERVER__WORKERS=1

EXPOSE 8080

COPY entrypoint.sh /root/

ENTRYPOINT ["/bin/bash", "/root/entrypoint.sh"]
