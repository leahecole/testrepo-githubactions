from airflow.operators.bash_oerator import BashOperator
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator
from airflow.providers.google.cloud.operators.gcs import GCSDeleteBucketOperator
from airflow import models
import uuid
import os
from airflow.utils.dates import days_ago
from airflow.utils.state import State
UUID = uuid.uuid4()
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "leah-playground")
BUCKET_NAME = f"leah-{UUID}"

with models.DAG(
    "example_gcs",
    start_date=days_ago(1),
    schedule_interval=None,
) as dag:
    create_bucket = GCSCreateBucketOperator(task_id="create_bucket", bucket_name=BUCKET_NAME, project_id=PROJECT_ID)

    list_objects = GCSListObjectsOperator(task_id="list_objects", bucket=BUCKET_NAME)
    list_buckets_result = BashOperator(
        task_id="list_buckets_result",
        bash_command="echo \"{{ task_instance.xcom_pull('list_objects') }}\"",
    )
    delete_bucket = GCSDeleteBucketOperator(task_id="delete_bucket", bucket_name=BUCKET_NAME)

    create_bucket >> list_objects >> delete_bucket


if __name__ == "__main__":
    dag.clear(dag_run_state=State.NONE)
    dag.run()