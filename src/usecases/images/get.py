from fastapi import status

from src.schemas.response import Response
from src.services.image_service import ImageService
from src.services.s3_service import S3Service


class ImageGetUseCase:
    def __init__(self, user_id: str, image_id: str):
        self.user_id = user_id
        self.image_id = image_id
        self.image_service = ImageService()
        self.s3_service = S3Service()

    def execute(self):
        image_model = self.image_service.get_image(image_id=self.image_id, user_id=self.user_id)
        if not image_model:
            return Response(status_code=status.HTTP_404_NOT_FOUND, success=False, message="Image not found")
        presign_url =  self.s3_service.get_presign_url(key=image_model.image_s3_key)
        image_model.image_url = presign_url
        response_data = image_model.to_simple_dict()
        return Response(data=response_data)

