import boto3
import os
import io
import base64


class S3Client:
    def __init__(self):
        self.s3 = boto3.client("s3", endpoint_url=os.getenv("S3_URL"))

    def upload(self, file, login_id, service_type, filename):
        self.s3.upload_fileobj(
            file,
            os.getenv("S3_BUCKET"),
            "/".join([login_id, service_type, filename]),
        )

    def upload_file_from_base64_string(
        self, base64_string, login_id, service_type, filename
    ):
        with io.BytesIO(bytes(base64.b64decode(base64_string))) as file:
            self.upload(
                file=file,
                login_id=login_id,
                service_type=service_type,
                filename=filename,
            )
