from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.settings import dbsettings

DB_USER = dbsettings.DB_USER
DB_PASSWORD = dbsettings.DB_PASSWORD
DB_HOST = dbsettings.DB_HOST
DB_PORT = dbsettings.DB_PORT
DB_NAME = dbsettings.DB_NAME

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
