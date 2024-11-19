from pydantic import BaseModel
from typing import Optional


class ImageUploadSchema(BaseModel):
    file_name: str
    file_size: float


class ListImagesSchema(BaseModel):
    page: int = 1
    limit: int = 10
    name: Optional[str] = None
    min_size: Optional[int] = None

