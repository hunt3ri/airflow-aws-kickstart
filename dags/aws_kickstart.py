import logging
import os
from datetime import timedelta

from airflow.sdk import Param, dag, task

logger = logging.getLogger("aws_kickstart_dag")


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


# Instantiate the DAG
aws_kickstart_dag()
