from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.load_config import db_settings

engine = create_engine(db_settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
