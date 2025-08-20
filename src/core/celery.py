# cho docker
# import gevent.monkey
# gevent.monkey.patch_all()
from celery import Celery
from src.config.conf import Configuration
from src.tasks import crawl_image_tasks
from src.tasks import zip_tasks
from src.tasks import chord_task
from src.tasks import workflow_task
from src.core.celeryconfig import schedule
config = Configuration()
# Cần sửa

celery = Celery(
    'PythonBE',
    broker= config.host_redis_not_docker,
    backend= f'db+{config.db_not_docker}',
    # include=[config.module_include]
)
celery.conf.beat_schedule = schedule
# Sửa lỗi pickle
celery.conf.update(
    task_serializer='json',
    result_serializer='json', # Quan trọng nhất
    accept_content=['json'],
    worker_pool='gevent'
)
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