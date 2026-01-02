### Install Airflow
```bash
# Set Airflow Home (optional)
# export AIRFLOW_HOME=~/airflow

# install airflow
uv add apache-airflow

# create folder for dags in the project
mkdir dags
# create folder for dags in the airflow home
mkdir -p ~/airflow/dags
# create symlink from project dags to airflow home dags
ln -s  "$(pwd)/dags" ~/airflow/dags/my_project

# start airflow server
airflow standalone

# open airflow in the browser http://localhost:8080
```
