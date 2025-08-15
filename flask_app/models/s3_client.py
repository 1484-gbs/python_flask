import boto3
import os


class S3Client:
    def __init__(self):
        self.s3 = boto3.client("s3", endpoint_url=os.getenv("S3_URL"))

    def upload(self, file, login_id, service_type, filename):
        self.s3.upload_fileobj(
            file,
            os.getenv("S3_BUCKET"),
            "/".join([login_id, service_type, filename]),
        )
