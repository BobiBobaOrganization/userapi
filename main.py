import logging
import fastapi as FastAPI
from contextlib import asynccontextmanager
from fastapi.params import Depends
from typing_extensions import Annotated
 
from config import get_settings, Settings
from src.api import users
from src.middlewares import error_handler
from src.dependencies import get_user_storage

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

@asynccontextmanager
async def lifespan(app: FastAPI.FastAPI):
    logging.info("FastAPI is starting up...")
    
    yield
    logging.info("FastAPI is shutting down...")

app = FastAPI.FastAPI(
    title="userapi",
    description="API for user management",
    version=get_settings().APPLICATION_VERSION,
    contact={
        "name": "Maksym Maliutin",
        "email": "maksym.maliutin@student.karazin.ua",
    },
    lifespan=lifespan, 
)
app.include_router(users.router)

app.add_middleware(error_handler.ErrorHandlerMiddleware)
error_handler.setup_exception_handlers(app)

get_user_storage()

@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "application_version": settings.APPLICATION_VERSION,
        "test_mode": settings.TEST_MODE
    }

@app.get("/")
async def read_root():
    return {"message": "FastAPI is running!"}