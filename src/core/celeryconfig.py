from celery.schedules import crontab

schedule = {
    'add-every-20-seconds': {
        'task': 'src.tasks.crawl_image_tasks.implement_crawl',
        'schedule': 20.0,
        'args': ('https://edition.cnn.com/',),
    },
}