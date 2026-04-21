from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="dbt_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command="cd /usr/app && dbt debug"
    )

    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command="cd /usr/app && dbt seed"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /usr/app && dbt run"
    )

    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command="cd /usr/app && dbt snapshot"
    )

    dbt_debug >> dbt_seed >> dbt_run >> dbt_snapshot