from src.models.images import InstaImageModel
from src.schemas.response import Response
from src.services.image_service import ImageService
from src.services.s3_service import S3Service
from src.setup import logger
from src.schemas.image import ListImagesSchema


class ImageListUseCase:
    def __init__(self, user_id: str, schema: ListImagesSchema):
        self.user_id = user_id
        self.image_service = ImageService()
        self.schema = schema
        self.s3_service = S3Service()

    def execute(self):
        filter_conditions = None
        if self.schema.name:
            filter_conditions = InstaImageModel.name.contains(str(self.schema.name))
        if self.schema.min_size:
            filter_conditions &= InstaImageModel.size >= self.schema.min_size

        images = self.image_service.list_images(
            hash_key=self.user_id,
            filter_condition=filter_conditions,
            page=self.schema.page,
            limit=self.schema.limit,
        )
        response_data = []
        for image in images:
            try:
                image.image_s3_key = self.s3_service.get_presign_url(key=image.image_s3_key)
                response_data.append(image.to_simple_dict())
            except Exception as ex:
                logger.error(f"Exception: {ex}", exc_info=True)
        return Response(data=response_data)
