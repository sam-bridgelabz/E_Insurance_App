from app.tasks.celery_worker import celery_app
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'send-expiry-reminder-every-day': {
        'task': 'app.tasks.email_reminder.send_expiry_reminder',
        'schedule': crontab(hour=9, minute=0),
    },
}