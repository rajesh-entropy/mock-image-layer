from fastapi import status

from src.schemas.response import Response
from src.services.image_service import ImageService
from src.services.s3_service import S3Service


class ImageDeleteUseCase:
    def __init__(self, user_id: str, image_id: str):
        self.user_id = user_id
        self.image_id = image_id
        self.image_service = ImageService()
        self.s3_service = S3Service()

    def execute(self):
        delete_status, message = self.image_service.delete_image(self.user_id, self.image_id)
        if delete_status:
            return Response(status_code=status.HTTP_200_OK, success=True, message=message)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND, success=False, message=message)
