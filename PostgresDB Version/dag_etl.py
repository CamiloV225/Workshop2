from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain
from datetime import datetime
from etl import read_csv, read_db, transform_db, transform_csv, merge

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 8),  # Update the start date to today or an appropriate date
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

def func1():
    print(f"the date is: {datetime.now()}")

with DAG(
    'dag_project',
    default_args=default_args,
    description='Workshop2',
    schedule_interval='@daily',  # Set the schedule interval as per your requirements
) as dag:

    merge = PythonOperator(
        task_id='merge',
        python_callable=merge,
        provide_context = True,
        )

    read_csv = PythonOperator(
        task_id='read_csv',
        python_callable=read_csv,
        provide_context = True,
        )

    transform_csv = PythonOperator(
        task_id='transform_csv',
        python_callable=transform_csv,
        provide_context = True,
        )

    read_db = PythonOperator(
        task_id='read_db',
        python_callable=read_db,
        provide_context = True,
        )

    transform_db = PythonOperator(
        task_id='transform_db',
        python_callable=transform_db,
        provide_context = True,
        )

    store = PythonOperator(
        task_id='store',
        python_callable=func1,
        provide_context = True,
        )

    load = PythonOperator(
        task_id='load',
        python_callable=func1,
        provide_context = True,
        )

    read_csv >> transform_csv >> merge >> load >> store
    read_db >> transform_db >> merge