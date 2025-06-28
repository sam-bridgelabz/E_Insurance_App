from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth.role_checker import employee_required
from app.config.logger_config import func_logger
from app.db.session import get_db
from app.exceptions.orm import AgentNotFound, DatabaseIntegrityError, EmailAlreadyExists
from app.models import agent_model
from app.schemas import agent_schema
from app.utils.hash_password import Hash

agent_router = APIRouter(prefix="/agent", tags=["Agent"])


@agent_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=agent_schema.ShowAgent
)
def create_agent(
    request: agent_schema.CreateAgent,
    db: Session = Depends(get_db),
    current_user: dict = Depends(employee_required),
):
    func_logger.info("POST /agent - Create new Agent!")

    try:
        existing_email = (
            db.query(agent_model.Agent)
            .filter(agent_model.Agent.email == request.email)
            .first()
        )
        if existing_email:
            func_logger.error(f"Email already exists: {request.email}")
            raise EmailAlreadyExists(detail=f"Email already exists: {request.email}")

        agent_data = request.model_dump()
        agent_data["password"] = Hash.get_hash_password(request.password)
        agent_data["emp_id"] = current_user["user"].id

        new_agent = agent_model.Agent(**agent_data)

        db.add(new_agent)
        db.flush()
        db.commit()
        db.refresh(new_agent)

        return new_agent

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error(f"❌ Database error during agent creation!: {e}")
        raise DatabaseIntegrityError()


@agent_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[agent_schema.ShowAgent]
)
def get_all_agents(
    db: Session = Depends(get_db), current_user: dict = Depends(employee_required)
):
    func_logger.info("GET /agent - Get list of Agents!")
    agents = db.query(agent_model.Agent).all()
    return agents


@agent_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_agent_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(employee_required),
):
    func_logger.info(f"GET /agent/{id} - Get Agent Details!")
    agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == id).first()

    if not agent:
        func_logger.error(f"❌The agent is not present: {id}")
        raise AgentNotFound(detail=f"The agent is not present: {id}")

    return agent


@agent_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_agent(
    id: str,
    request: agent_schema.UpdateAgent,
    db: Session = Depends(get_db),
    current_user: dict = Depends(employee_required),
):
    func_logger.info(f"PUT /agent/{id} - Update Agent Details!")

    try:
        agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == id)
        if not agent.first():
            func_logger.error(f"❌The agent is not present: {id}")
            raise AgentNotFound(detail=f"The agent is not present: {id}")

        update_data = request.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = Hash.get_hash_password(update_data["password"])

        agent.update(update_data)
        db.commit()

        func_logger.info(f"Agent updated successfully: {id}")
        return {
            "message": f"Agent updated successfully: {id}",
            "status": status.HTTP_202_ACCEPTED,
        }

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error(f"❌ Database error during agent update: {e}")
        raise DatabaseIntegrityError()


@agent_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_agent(
    id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(employee_required),
):
    func_logger.info(f"DELETE /agent/{id} - Delete Agent!")
    try:
        agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == id)

        if not agent.first():
            func_logger.error(f"❌The agent is not present: {id}")
            raise AgentNotFound(detail=f"The agent is not present: {id}")

        agent.delete(synchronize_session=False)
        db.commit()

        func_logger.info(f"Agent deleted successfully: {id}")
        return {
            "message": f"Agent deleted successfully: {id}",
            "status": status.HTTP_200_OK,
        }

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error(f"❌ Database error during agent deletion: {e}")
        raise DatabaseIntegrityError()
