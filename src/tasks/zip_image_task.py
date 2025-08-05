from celery import shared_task
from typing import List
from ..services.get_images import GetImageService
import os
get_image_services = GetImageService()

@shared_task(name="zip")
def down_zip_image(list_url: List[str], save_dir, zip_name):
    path_zip = get_image_services.download_and_zip_images(list_url, save_dir, zip_name)
    filename = os.path.basename(path_zip)
    return f"/public/{filename}"
    
# down_zip_image()
# print("zip_image_task.py loaded")

# down_zip_image.delay('https://kenh14cdn.com/zoom/250_156/203336854389633024/2025/7/31/avatar1753928712229-1753928712793777074506-0-99-630-1107-crop-1753928759420549968873.webp',
#                      'public', '1')