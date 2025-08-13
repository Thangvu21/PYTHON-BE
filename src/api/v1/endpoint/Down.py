from fastapi.concurrency import run_in_threadpool
from src.models.TimeRange import TimeRange
from fastapi import APIRouter
from src.tasks.zip_tasks import zipFolder
from uuid import uuid4
from src.services.image_services import ImageModel
from src.services.get_images import GetImageService

image_services = ImageModel()
get_image_services = GetImageService()

router = APIRouter(prefix='/down', tags=['down_image'])

@router.post('/down_zip')
async def down_load_zip(time_range: TimeRange):
    # images_for_time = image_services.get_images_for_time(time_range.start_time, time_range.end_time)
    images_for_time = await run_in_threadpool( 
        image_services.get_images_for_time,
        time_range.start_time, 
        time_range.end_time
    )
    url_for_time = [image['url'] for image in images_for_time]
    path_zip = await get_image_services.download_and_zip_images(url_for_time, 'src/public', str(uuid4()))
    return f"http://localhost:8000/{path_zip}"



#download ảnh 
# Tạo endpoint cơ chế yêu cầu
@router.post('/down_load_zip')
async def down_load_zip_api(time_range: TimeRange):
    images_for_time = image_services.get_images_for_time(time_range.start_time, time_range.end_time)
    images_for_time = await run_in_threadpool( 
        image_services.get_images_for_time,
        time_range.start_time, 
        time_range.end_time
    )
    url_for_time = [image['url'] for image in images_for_time]
    task = zipFolder.delay(url_for_time, 'public', str(uuid4()))
    return {"task_id": task.id}

# Tạo endpoint cơ chế hỏi để kiểm tra
@router.get('/task_status')
async def get_task_status(task_id: str):
    task = zipFolder.AsyncResult(task_id)
    if task.state == "PENDING":
        return {"status": "pending"}
    elif task.state == 'SUCCESS':
        return {
            "status": "success",
            "download_url": f"http://localhost:8000/{task.result}"
        }
    elif task.state == 'FAILURE':
        return {"status": "failure", "error": str(task.info)}
    else:
        return {"status": task.state}
