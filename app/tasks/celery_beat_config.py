from celery.schedules import crontab

from app.tasks.celery_worker import celery_app

celery_app.conf.beat_schedule = {
    "send-expiry-reminder-every-day": {
        "task": "app.tasks.email_reminder.send_expiry_reminder",
        "schedule": crontab(hour=9, minute=0),
    },
    "daily-db-backup-at-2am": {
        "task": "app.tasks.backup_task.backup_postgres",
        "schedule": crontab(hour=2, minute=0),  # runs every day at 2:00 AM
    },
}
