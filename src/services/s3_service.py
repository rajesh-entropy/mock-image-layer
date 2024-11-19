import boto3
from botocore.config import Config

from src.config import Configuration
from src.setup import logger
from src.constants import Constants


class S3Service:
    GET_OBJECT = "get_object"
    PUT_OBJECT = "put_object"
    DEFAULT_EXPIRATION = 3600

    def __init__(self, region_name=Configuration.REGION):
        self.s3_client = boto3.client(
            "s3",
            config=Config(signature_version="s3v4"),
            region_name=region_name,
            endpoint_url=Configuration.LOCALSTACK_URL
        )
        self.s3_resource = boto3.resource("s3")

    def get_presign_url(
            self,
            key: str,
            bucket_name: str = Constants.IMAGE_BUCKET,
            expiration: int = DEFAULT_EXPIRATION,
            request_type: str = GET_OBJECT
    ):
        """
        Generate a pre-signed URL for uploading data to S3
        :param bucket_name:
        :param key:
        :param expiration:
        :param request_type:
        :return:
        """
        try:
            response = self.s3_client.generate_presigned_url(
                request_type=request_type,
                Params={"Bucket": bucket_name, "Key": key},
                ExpiresIn=expiration,
            )
            return response
        except Exception as ex:
            logger.error("Error while generating pre-signed URL", ex)
            raise ex

    def upload_media_to_s3(
        self, bucket_name: str, file_path: str, body: bytes, content_type: str
    ) -> bool:
        try:
            self.s3_client.put_object(
                Bucket=bucket_name, Key=file_path, Body=body, ContentType=content_type
            )
            return True
        except Exception as ex:
            logger.error(f"Exception: {ex}", exc_info=True)
            return False

    def download_file_from_s3(self, file_path, bucket, key):
        self.s3_client.download_file(bucket, key, file_path)

    def delete_file_from_s3(self, bucket, key):
        self.s3_client.delete_object(Bucket=bucket, Key=key)

