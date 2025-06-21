from sqlalchemy.orm import Session
from app.models.scheme import Scheme


class SchemeQueries:

    @staticmethod
    def get_by_id(db: Session, scheme_id: int) -> Scheme | None:
        return db.query(Scheme).filter(Scheme.id == scheme_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Scheme | None:
        return db.query(Scheme).filter(Scheme.name == name).first()
