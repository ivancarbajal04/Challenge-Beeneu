from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from loguru import logger
import settings, uvicorn

from apis.users.router import router as users_router
from apis.statistics.router import router as statistics_router

def init_app():
    logger.info(f"Starting {settings.project_name}")

    api = FastAPI(
        title=settings.project_name,
        version=settings.project_version,
        debug=settings.debug,
        redirect_slashes=False
    ) 
    
    api.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    api.include_router(users_router)
    api.include_router(statistics_router)
    
    logger.info(f"{settings.project_name} successfully initialized")
    
    return api


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
