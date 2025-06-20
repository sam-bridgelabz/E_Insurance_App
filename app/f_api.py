from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.logger_config import config_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        config_logger.info("🚀App is starting up...")

    except Exception as e:
        config_logger.exception(f"❌ Error in the startup stage: {e}")

    yield

    print("🙏 App shutting down...")


#App metadata
f_api = FastAPI(
    title="E-Insurance Management System",
    description="A role-based insurance system built with FastAPI.",
    version="1.0.0",
    contact={
        "name": "Monocept Team",
        "url": "https://github.com/sam-bridgelabz/E_Insurance_App",
        "email": "sam.varghese@bridgelabz.com"
    },
    lifespan=lifespan
)
