from src.services.image_service import ImageService
from src.schemas.image import ImageUploadSchema
from src.schemas.response import Response
from src.setup import logger
from fastapi import status


class ImageUploadUseCase:
    def __init__(self, user_id: str, schema: ImageUploadSchema):
        self.user_id = user_id
        self.image_schema = schema
        self.image_service = ImageService()

    def execute(self):
        try:
            presign_url = self.image_service.entry_for_image(user_id=self.user_id, schema=self.image_schema)
            return Response(message="Image entry created successfully",
                            data={"presign_url": presign_url})
        except Exception as ex:
            logger.error(f"Exception: {ex}", exc_info=True)
            return Response(
                success=False,
                message="Error while uploading image",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
