import json
import os.path
from contextlib import closing
from pathlib import Path
from threading import Event

import boto3
import requests
from botocore.exceptions import ClientError
from rich.progress import (
    BarColumn, 
    DownloadColumn, 
    Progress, 
    TextColumn, 
    TimeRemainingColumn, 
    TransferSpeedColumn
)

from src import logging

logger = logging.getLogger(__name__)

class AWSUtils:
    """Manages AWS operations including S3, Secrets Manager, and SSM Parameter Store."""
    
    def __init__(self, region: str = "us-east-1", account_id: str = "641949442254"):
        self.region = region
        self.account_id = account_id
        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )
        self.done_event = Event()
        
        # Initialize AWS clients
        self.s3_client = boto3.client("s3", region_name=self.region)
        self.s3_resource = boto3.resource("s3", region_name=self.region)
        self.ssm_client = boto3.client("ssm", region_name=self.region)
        self.secrets_client = boto3.client("secretsmanager", region_name=self.region)

    async def download_file_s3(self, bucket: str, filename: str, dest_dir: str) -> None:
        """Download a file from S3 to a local file with progress tracking."""
        with self.progress:
            file = filename.split("/")[-1]
            path = os.path.join(dest_dir, file)
            task_id = self.progress.add_task("download", filename=file, start=False)
            self.progress.console.log(f"Starting download for s3://{bucket}/{filename}")
            
            try:
                total_size = self.s3_client.head_object(Bucket=bucket, Key=filename)["ContentLength"]
                if task_id is not None:
                    self.progress.update(task_id, total=total_size)

                def download_chunk(bytes_transferred):
                    if task_id is not None:
                        self.progress.update(task_id, advance=bytes_transferred)

                with open(path, "wb") as dest_file:
                    if task_id is not None:
                        self.progress.start_task(task_id)
                    self.s3_client.download_fileobj(
                        Bucket=bucket,
                        Key=filename,
                        Fileobj=dest_file,
                        Callback=download_chunk
                    )
                    if self.done_event.is_set():
                        return
                self.progress.console.log(f"Downloaded {path}")
            except Exception as e:
                self.progress.console.log(f"Failed to download s3://{bucket}/{filename}: {e}")

    async def upload_file_s3(self, bucket: str, filename: str, path: str | Path) -> str:
        """Upload a local file to S3."""
        self.s3_resource.meta.client.upload_file(
            Bucket=bucket,
            Key=filename,
            Filename=str(path)
        )
        return f"s3://{bucket}/{filename}"

    async def upload_stream_file_s3(
        self,
        bucket: str,
        filename: str,
        url: str,
        content_type: str = "video/mp4"
    ) -> None:
        """Upload a file to S3 from a URL stream."""
        logger.info(f"Uploading file:{filename} to s3:{url}")
        with closing(requests.get(url, stream=True)) as r:
            self.s3_resource.meta.client.upload_fileobj(
                r.raw,
                bucket,
                filename,
                ExtraArgs={"ContentType": content_type}
            )

    def get_aws_secret(self, secret_name: str) -> dict:
        """Retrieve a secret from AWS Secrets Manager."""
        try:
            response = self.secrets_client.get_secret_value(SecretId=secret_name)
            secrets = json.loads(response["SecretString"])
            return secrets
        except ClientError as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            raise
        except KeyError:
            logger.error("Received unexpected data format from Secrets Manager.")
            raise

    def create_aws_secret(self, secret_name: str, secret_value: str, description: str = None) -> None:
        """Create a secret in AWS Secrets Manager."""
        try:
            response = self.secrets_client.create_secret(
                Name=secret_name,
                SecretString=secret_value,
                Description=description
            )
            logger.info(f"Secret created: {response['ARN']}")
        except ClientError as e:
            logger.error(f"An error occurred: {e}")

    def create_ssm_parameter(
        self,
        name: str,
        value: str,
        description: str = None,
        param_type: str = "SecureString"
    ) -> None:
        """Create or update a parameter in AWS SSM Parameter Store."""
        if not name.startswith("/"):
            name = f"/prod/{name.lower()}"

        try:
            response = self.ssm_client.put_parameter(
                Name=name,
                Value=value,
                Description=description,
                Type=param_type,
                Overwrite=True
            )
            logger.info(f"Parameter created/updated parameter:{name} version:{response['Version']}")
        except ClientError as e:
            logger.error(f"An error occurred: {e}")

    def get_ssm_parameter(self, name: str, with_decryption: bool = True) -> str | None:
        """Fetch a parameter from AWS SSM Parameter Store."""
        if not name.startswith("arn:aws:"):
            name = f"arn:aws:ssm:{self.region}:{self.account_id}:parameter/prod/{name.lower()}"

        try:
            response = self.ssm_client.get_parameter(
                Name=name,
                WithDecryption=with_decryption
            )
            value = response["Parameter"]["Value"]
            logger.info(value)
            return value
        except ClientError as e:
            logger.error(f"An error occurred: {e}")
            return None


if __name__ == "__main__":
    aws_manager = AWSUtils()
    res = aws_manager.get_ssm_parameter("OPENAI_API_KEY")
