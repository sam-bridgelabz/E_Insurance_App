from app.config.config import APISettings, DBSettings, RedisSettings, SMTPSettings

db_settings = DBSettings()
api_settings = APISettings()
smtp_settings = SMTPSettings()
redis_settings = RedisSettings()

if __name__ == "__main__":
    print(db_settings)
    print(api_settings)
    print(smtp_settings)
