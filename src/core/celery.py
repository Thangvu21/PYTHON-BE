from celery import Celery
from src.config.conf import Configuration
from src.tasks import crawl_image_tasks
from src.core.celeryconfig import schedule
config = Configuration()
# Cần sửa
host_redis = config.host_redis_not_docker

celery = Celery(
    'PythonBE',
    broker= host_redis,
    backend= host_redis,
    # include=[config.module_include]
)
celery.conf.beat_schedule = schedule
celery.conf.timezone = 'Asia/Ho_Chi_Minh'

celery.autodiscover_tasks(['src.tasks'])
# include này là một loạt module được import khi worker start
# chỉ nhận module thôi ko nhận package
# celery.conf.result_backend = 'db+sqlite:///results.sqlite' config thêm để dùng phương thức async

celery.conf.update(
    result_expires = 3600,
)

if __name__ == '__main__':
    celery.start()