from app.database import Base, engine


# Initialize the DB
class DBInitialize:

    @staticmethod
    def create_tables():
        Base.metadata.create_all(bind=engine)
