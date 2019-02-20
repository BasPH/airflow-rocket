<img style="float: right;" src="rocket.png">

# Airflow Rocket

This repository contains code accompanying ~this Airflow blog post series~WIP. To get started, run `docker run -d -p 8080:8080 basph/airflow-rocket`.

Throughout the blog post series, I explain various Airflow concepts and give examples using the [Launch Library API](https://launchlibrary.net/docs/1.4/api.html), hence the repository name "Airflow Rocket". 

**IMPORTANT**: The Dockerfile in this repository creates a single image containing all Airflow components, and examples and demos shown in the blog post. It is **NOT** intended for production usage! For more information on running Airflow in production, read the [blog post part 4](https://blog.godatadriven.com).

If you mount your own DAGs volume, the container takes 10-15 seconds to start up. This is because `airflow initdb` is executed at startup (if no `.airflow-rocket` file was found in the DAGs folder). The idea is to clear all built-in DAGs and only display your own, mounted, DAGs.

Versions used:

- Airflow 1.10.2
- Python 3.6.6
- Launch Library API 1.4

<div style="font-size: 12px;">Rocket icon made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>, licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a>.</div>
