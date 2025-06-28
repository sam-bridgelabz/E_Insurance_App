# to run celery
# celery -A app.tasks.celery_worker.celery_app worker --pool=solo --loglevel=info
# celery -A app.tasks.celery_worker.celery_app beat --loglevel=info

from celery import Celery

from app.config.load_config import redis_settings

celery_app = Celery(
    "e_insurance", broker=redis_settings.REDIS_URL, backend=redis_settings.REDIS_URL
)

celery_app.conf.timezone = "UTC"

from app.tasks import celery_beat_config
