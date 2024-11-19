from pydantic import BaseModel


class ImageUploadSchema(BaseModel):
    file_name: str
    file_size: float


class ListImagesSchema(BaseModel):
    page: int = 1
    limit: int = 10
    name: str = None
    min_size: float = None

