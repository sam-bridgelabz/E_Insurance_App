from sqlalchemy.orm import Session
from app.models.scheme_model import Scheme
from app.models.policy_model import Policy

class SchemeQueries:

    @staticmethod
    def get_by_id(db: Session, scheme_id: int) -> Scheme | None:
        return db.query(Scheme).filter(Scheme.id == scheme_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Scheme | None:
        return db.query(Scheme).filter(Scheme.name == name).first()
    
class PolicyQueries:

    @staticmethod
    def get_by_id(db: Session, scheme_id: int) -> Policy | None:
        return db.query(Policy).filter(Policy.id == scheme_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Policy | None:
        return db.query(Policy).filter(Policy.name == name).first() 
