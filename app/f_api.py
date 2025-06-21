from contextlib import asynccontextmanager

from app.config.logger_config import config_logger
from app.routes import admin, agent, employee, auth
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        config_logger.info("🚀App is starting up...")

    except Exception as e:
        config_logger.exception(f"❌ Error in the startup stage: {e}")

    yield

    print("🙏 App shutting down...")


# App metadata
f_api = FastAPI(
    title="E-Insurance Management System",
    description="A role-based insurance system built with FastAPI.",
    version="1.0.0",
    contact={
        "name": "Monocept Team",
        "url": "https://github.com/sam-bridgelabz/E_Insurance_App",
        "email": "sam.varghese@bridgelabz.com",
    },
    lifespan=lifespan,
)


f_api.include_router(auth.login_router)
f_api.include_router(auth.user_router)
f_api.include_router(admin.admin_router)
f_api.include_router(employee.employee_router)
f_api.include_router(agent.agent_router)
