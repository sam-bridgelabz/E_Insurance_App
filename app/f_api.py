from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.db_initialize import DBInitialize
from app.config.logger_config import config_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        config_logger.info("🚀App is starting up...")
        DBInitialize.create_tables()
        config_logger.info("📍Database tables created/checked successfully!!!")

    except Exception as e:
        config_logger.exception(f"❌ Error in the startup stage: {e}")

    yield

    print("🙏 App shutting down...")


f_api = FastAPI(lifespan=lifespan)
