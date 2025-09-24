import logging
import os
from datetime import timedelta

from airflow.sdk import Param, dag, task

logger = logging.getLogger("aws_kickstart_dag")

@task(
    task_id="list_buckets",
    execution_timeout=timedelta(seconds=20),
    retries=3,
    retry_delay=timedelta(seconds=5)
)
def list_buckets(dag_params: dict) -> dict:
    """ List S3 buckets based on DAG parameters """
    # IMPORTANT - Imports must be inside the task to avoid pickle issues with Airflow
    from services.s3_service import S3Service

    s3_service = S3Service.from_airflow_task(dag_params)
    s3_service.handle_request()


@dag(
    dag_id="aws_kickstart",
    catchup=False,
    schedule=None,
    tags=["apps", "aws"],
    max_active_runs=1,
    max_active_tasks=1,
    params={
        "list_all_buckets": Param(
            default=True,
            type="boolean",
            title="List All S3 Buckets",
            description="Set to true to list all S3 buckets in the account"
        ),
        "bucket_name": Param(
            default="",
            type=["null", "string"],  # Allow null meaning param is optional
            title="S3 Bucket Name",
            description="If List All Buckets is false, specify the S3 bucket name to list",
        ),
    }
)
def aws_kickstart_dag() -> None:
    """ DAG to demo interacting with AWS services """

    @task
    def parse_dag_params(**context: dict) -> dict:
        """Extract DAG parameters from context and pass to tasks that are declared outside the DAG function"""
        logger.info("Parsing DAG params")
        return {
            'list_all_buckets': context['params']['list_all_buckets'],
            'bucket_name': context['params']['bucket_name'],
        }

    # Define the workflow here
    dag_params = parse_dag_params()
    list_buckets(dag_params)


# Instantiate the DAG
aws_kickstart_dag()
