from fastapi.concurrency import run_in_threadpool
from src.models.TimeRange import TimeRange
from fastapi import APIRouter
from src.tasks.zip_tasks import zipFolder
from uuid import uuid4
from src.services.image_services import ImageModel
from src.services.get_images import get_image_services
from src.services.image_services import image_services
from src.tasks.chord_task import pipeline_v2
from src.tasks.workflow_task import pipeline_v3
from celery.result import AsyncResult
import os
from src.config.broker import r

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

@router.post('/chord_image')
async def chord_down_api(time_range: TimeRange):
    task = pipeline_v2.delay(time_range.start_time, time_range.end_time, 'src/public', str(uuid4()))
    return {"task_id": task.id}

@router.get('/chord_status/{task_id}')
async def chord_status(task_id: str):
    task = AsyncResult(task_id)
    if task.state == "PENDING":
        return {"status": "pending"}
    elif task.state == 'SUCCESS':
        result_task = task.get()
        print(f"result_task: {result_task}")
        zip_filename = os.path.basename(result_task)
    
        return {"status": "success", "download_url": f"http://localhost:8000/public/{zip_filename}"}
    elif task.state == 'FAILURE':
        return {"status": "failure", "error": str(task.info)}
    else:
        return {"status": task.state}
    
@router.post('/chord_image_gevent')
async def chord_down_api(time_range: TimeRange):
    task = pipeline_v3.delay(time_range.start_time.isoformat(), time_range.end_time.isoformat(), 'src/public')
    return {"task_id": task.id}

@router.get('/chord_status_gevent/{task_id}')
async def chord_status(task_id: str):
    task = AsyncResult(task_id)
    if task.state == "PENDING":
        done = float(r.hget(f"progress: {task_id}", "done") or 0)
        total = float(r.hget(f"progress: {task_id}", "total") or 1)
        progress = done / total * 100
        return {"done": done, "total": total, "progress": progress, "status": "PENDING"}

    elif task.state == 'SUCCESS':
        result_task = task.get()
        print(f"result_task: {result_task}")
        zip_filename = os.path.basename(result_task)
    
        return {"status": "SUCCESS", "download_url": f"http://localhost:8000/public/{zip_filename}"}
    elif task.state == 'FAILURE':
        return {"status": "failure", "error": str(task.info)}
    else:
        return {"status": task.state}