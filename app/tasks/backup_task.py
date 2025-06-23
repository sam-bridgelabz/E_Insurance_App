import os
import subprocess
from datetime import datetime
from celery import shared_task
from app.config.load_config import db_settings


@shared_task
def backup_postgres():
    db_name = db_settings.POSTGRESQL_DATABASE
    db_user = db_settings.POSTGRESQL_USERNAME
    db_password = db_settings.POSTGRESQL_PASSWORD
    db_host = db_settings.POSTGRESQL_SERVER
    db_port = str(db_settings.POSTGRESQL_PORT)

    backup_dir = "backups/"
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{backup_dir}/backup_{timestamp}.sql"

    os.environ["PGPASSWORD"] = db_password

    try:
        subprocess.run(
            ["pg_dump", "-h", db_host, "-p", db_port, "-U", db_user, "-d",
             db_name, "-f", filename],
            check=True
        )
        print(f"✅ Backup successful: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backup failed: {e}")
    finally:
        del os.environ["PGPASSWORD"]
