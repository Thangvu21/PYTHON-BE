from celery import shared_task
from typing import List
import asyncio
import os
from celery.utils.log import get_task_logger
from src.services.get_images import get_image_services
logger = get_task_logger(__name__)


# Task kế thừa task để triển khai thứ liên quan đến khi lỗi hiển thị như nào

# @shared_task(name="down_image_task", bind=True)
# async def downImageTask(self, url: str, save_path: str):
#     logger.info(f'exexute async down_image_task {self.request.id}')
#     return await asyncio.run(get_image_services.downImage(url, save_path))

# @shared_task(name="down_list_image_task", bind=True)
# async def downListImageTask(self, list_url: List[str], save_path):
#     logger.info(f'exexute async down_list_image_task {self.request.id}')
#     return await asyncio.run(get_image_services.downListImages(list_url, save_path))

@shared_task(name="zip_folder_task", bind=True)
def zipFolder(self, list_url: List[str], save_path: str, zip_name: str):
    logger.info(f'exexute async down_zip_task {self.request.id}')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abs_save_path = os.path.join(BASE_DIR, save_path)
    logger.info(f'abs_save_path: {abs_save_path}')
    try:
        result = asyncio.run(
            get_image_services.download_and_zip_images(
                list_url, abs_save_path, zip_name
        ))
        logger.info(f'Zip created at: {result}')
        return result
    except Exception as e:
        logger.error(f'Error in zipFolder: {e}')
        


