import logging

import boto3
from services.utils import get_streaming_logger

logger = get_streaming_logger("s3_service")

class S3Service:

    s3_client = None
    dag_params: dict = None
    logger: logging.Logger = None

    @classmethod
    def from_airflow_task(cls, dag_params: dict, is_called_from_venv: bool = False) -> "S3Service":
        """Create an instance of SSMService from an Airflow task"""
        # Instantiate the boto client in at the class level to avoid pickle issues with Airflow
        logger.info("Creating S3Service from Airflow task")
        cls.s3_client = boto3.client('s3')
        cls.dag_params = dag_params

        if is_called_from_venv:
            # If called from a virtualenv task, set up a streaming logger
            cls.logger = get_streaming_logger("s3_service_venv")
        else:
            cls.logger = logging.getLogger("s3_service")


        return cls()

    def handle_request(self) -> None:
        """ Handle the request based on the DAG parameters """
        if self.dag_params['list_all_buckets']:
            self.list_all_buckets()
        else:
            bucket_name = self.dag_params['bucket_name']
            if not bucket_name:
                logger.error("Bucket name must be provided if list_all_buckets is false")
                raise ValueError("Bucket name must be provided if list_all_buckets is false")
            self.list_bucket(bucket_name)

    def list_bucket(self, bucket_name: str) -> None:
        """ List objects in a specific S3 bucket """
        logger.info(f"Listing objects in bucket: {bucket_name}")
        response = self.s3_client.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in response:
            for obj in response['Contents']:
                logger.info(f"Found object: {obj['Key']} (Size: {obj['Size']} bytes)")
            logger.info(f"Found {len(response['Contents'])} objects in bucket {bucket_name}")
        else:
            logger.info(f"No objects found in bucket {bucket_name}")


    def list_all_buckets(self) -> None:
        """ List all S3 buckets in the account """
        logger.info("Listing all S3 buckets in the account")
        response = self.s3_client.list_buckets()

        for bucket in response['Buckets']:
            logger.info(f"Found bucket: {bucket['Name']}")

        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        logger.info(f"Found {len(bucket_names)} buckets")
