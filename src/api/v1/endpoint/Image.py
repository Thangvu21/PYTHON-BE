from src.models.TimeRange import TimeRange
from fastapi.concurrency import run_in_threadpool
from fastapi import APIRouter
from src.api.v1.endpoint.Down import image_services

router = APIRouter(prefix="/image", tags=['get_image'])

@router.post("/image_for_time")
async def image_for_time(time_range: TimeRange):
    images_for_time = await run_in_threadpool( 
        image_services.get_images_for_time,
        time_range.start_time, 
        time_range.end_time
    )
    return images_for_time

@router.get("/images")
async def postUrl():
    list_images = await run_in_threadpool(image_services.get_all_images)
    return list_images

@router.get("/l_images")
async def limitUrl(page = 0, page_size = 20):
    list_images = await run_in_threadpool(image_services.get_offset_images,page, page_size)
    return list_images

@router.get("/number_pages")
async def number_pages(page_size = 20):
    # number_pages = image_services.get_pages(page_size=page_size)
    number_pages = await run_in_threadpool(image_services.get_pages, page_size)
    return number_pages


