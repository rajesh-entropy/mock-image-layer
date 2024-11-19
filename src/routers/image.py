from fastapi import APIRouter, Request
from src.schemas.response import Response
from src.schemas.image import ImageUploadSchema, ListImagesSchema
from src.usecases.images.upload import ImageUploadUseCase
from src.usecases.images.delete import ImageDeleteUseCase
from src.usecases.images.list import ImageListUseCase
from src.usecases.images.get import ImageGetUseCase

image_router_v1 = APIRouter(
    prefix="/v1",
    tags=["IMAGES"],
)


def get_user_id_from_headers(request: Request):
    # TODO keep this method in a common place
    # reading user id from headers
    context = request.state.context if hasattr(request.state, "context") else {}
    return context["user_id"]


@image_router_v1.post(path="/images", response_model=Response)
async def create_image(request: Request, body: ImageUploadSchema):
    user_id = get_user_id_from_headers(request)
    return ImageUploadUseCase(user_id=user_id, schema=body).execute()


@image_router_v1.get(path="/images", response_model=Response)
async def list_images(request: Request, name=None, size=None, page=1, limit=10):
    list_images_schema = ListImagesSchema(name=name, size=size, page=page, limit=limit)
    return ImageListUseCase(user_id=get_user_id_from_headers(request), schema=list_images_schema).execute()

@image_router_v1.get(path="/images/{image_id}", response_model=Response)
async def get_image(request: Request, image_id: str):
    return ImageGetUseCase(user_id=get_user_id_from_headers(request), image_id=image_id).execute()

@image_router_v1.delete(path="/images/{image_id}", response_model=Response)
async def delete_image(request: Request, image_id: str):
    return ImageDeleteUseCase(user_id=get_user_id_from_headers(request), image_id=image_id).execute()
