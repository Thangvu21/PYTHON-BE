from celery import shared_task
from src.services.crawl_services import CrawlImageService
from src.services.image_services import ImageModel, Image, List
from src.services.get_images import GetImageService
import os

        
# crawl trực t
@shared_task(name="crawl")
def implement_crawl(url):
    craw_service = CrawlImageService(url)
    imageModel = ImageModel()
    list_url = craw_service.crawl()
    print(f"list_url: {list_url}")
    list_url_image: List[Image] = [
        Image(url=url) for url in list_url
    ]
    print(f"list_url_image: {list_url_image}")
    return imageModel.add_images(list_url_image)
    
# dấu chấm để import 1 cái tương đối


get_image_services = GetImageService()

@shared_task(name="zip")
def down_zip_image(list_url: List[str], save_dir, zip_name):
    path_zip = get_image_services.download_and_zip_images(list_url, save_dir, zip_name)
    filename = os.path.basename(path_zip)
    return f"/public/{filename}"

# down_zip_image.delay('https://kenh14cdn.com/zoom/250_156/203336854389633024/2025/7/31/avatar1753928712229-1753928712793777074506-0-99-630-1107-crop-1753928759420549968873.webp',
#                      'public', '1')