from app.config.config import APISettings, DBSettings, SMTPSettings

db_settings = DBSettings()
api_settings = APISettings()
smtp_settings = SMTPSettings()


if __name__ == "__main__":
    print(db_settings)
    print(api_settings)
