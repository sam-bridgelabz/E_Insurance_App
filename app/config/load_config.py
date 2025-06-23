from app.config.config import APISettings, DBSettings

db_settings = DBSettings()
api_settings = APISettings()


if __name__ == "__main__":
    print(db_settings)
    print(api_settings)