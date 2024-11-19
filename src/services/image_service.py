from src.setup import logger
from src.models.images import InstaImageModel
from src.services.s3_service import S3Service
import uuid
from pynamodb.exceptions import DoesNotExist
from src.schemas.image import ImageUploadSchema
from typing import Tuple, Optional, List
from pynamodb.expressions.condition import Condition


class ImageService:
    def __init__(self):
        self.s3_service = S3Service()
        self.image_model = InstaImageModel

    @staticmethod
    def get_unique_image_id() -> str:
        """
        This method generates a unique image ID for the image.
        :return: unique image ID
        """
        return str(uuid.uuid4())

    @staticmethod
    def get_image_s3_key(user_id: str, image_id: str) -> str:
        """
        This method generates the S3 key for the image.
        :param user_id: user ID
        :param image_id: image ID
        :return: S3 key
        """
        return f"{user_id}/raw/{image_id}"

    def entry_for_image(self, user_id: str, schema: ImageUploadSchema):
        """
        This method creates entry for the image in the database and returns pre-signed URL for the image.
        :param user_id:
        :param schema:
        :return: pre-signed URL for the image
        """
        image_s3_key = self.get_image_s3_key(user_id, schema.file_name)
        image_model = self.image_model(
            user_id=user_id,
            image_id=schema.file_name,
            image_s3_key=image_s3_key,
            name=schema.file_name,
            size=schema.file_size,
            meta_data=schema.meta_data,
        )
        image_model.save()
        return self.s3_service.get_presign_url(key=image_s3_key, request_type=S3Service.PUT_OBJECT)

    def delete_image(self, user_id: str, image_id: str) -> Tuple[bool, str]:
        """
        This method deletes the image from the database and S3.
        :param user_id: user ID
        :param image_id: image ID
        :return: deletion status and message
        """
        try:
            image_model = self.image_model.get(hash_key=user_id, range_key=image_id)
            image_model.update(actions=[InstaImageModel.is_deleted.set(True)])
            # self.s3_service.delete_object(image_model.image_s3_key)
            logger.info(f"Image {image_model.image_s3_key} soft deleted successfully")
            return True, "Image deleted successfully"
        except DoesNotExist:
            logger.warning(f"Image not found with image_id: {image_id}, user_id: {user_id}")
            return False, "Image not found"
        except Exception as ex:
            logger.error(f"Error while deleting image, image_id: {image_id}, user_id: {user_id}", ex)
            return False, "Error while deleting image"

    def get_image(self, image_id: str, user_id: str) -> Optional[InstaImageModel]:
        try:
            image_model = self.image_model.get(hash_key=user_id, range_key=image_id)
            return image_model
        except DoesNotExist:
            logger.warning(f"Image not found with image_id: {image_id}, user_id: {user_id}")
            return None

    def list_images(
            self,
            hash_key: str,
            range_key_condition: Optional[Condition] = None,
            filter_condition: Optional[Condition] = None,
            page: int = 1,
            limit: int = 10
    ) -> List[
        InstaImageModel]:

        try:
            images = self.image_model.query(
                hash_key=hash_key,
                range_key_condition=range_key_condition,
                filter_condition=filter_condition,
                limit=limit,
                page_size=page
            )
            return [image for image in images]
        except Exception as ex:
            logger.error(f"Error while listing images, hash_key: {hash_key}", ex)
            return []
