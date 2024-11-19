from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from routers.image import image_router_v1

from setup import logger
from src.config import Configuration

insta_app = FastAPI(
    title="Insta Image REST API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Add routers
insta_app.include_router(image_router_v1)

@insta_app.get("/v1/health", tags=["base"])
async def main_route():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Server is up and running",
            "error": False,
            "success": True,
            "data": None,
        },
    )

if __name__ == "__main__":
    import uvicorn

    logger.info("Running Insta App")
    uvicorn.run(
        app="main:insta_app",
        host="0.0.0.0",
        port=Configuration.PORT,
        log_level=Configuration.LOG_LEVEL.lower(),
        reload=True,
    )
