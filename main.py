from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from uuid import uuid4
from pydantic import BaseModel
from src.services.image_services import ImageModel
from src.services.get_images import GetImageService
from src.tasks.crawl_image_tasks import implement_crawl
# from src.tasks.zip_image_task import down_zip_image
from src.core.celery import celery
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

templates = Jinja2Templates(directory="src/templates")
image_services = ImageModel()
get_image_services = GetImageService()

app =  FastAPI(title="ChimichangApp")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify domains like ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="src/static"), name="static")
# mount là nối từ thư mục đó qua http và post
app.mount("/public", StaticFiles(directory="src/public"), name='public')

class URL(BaseModel):
    url: str

class TimeRange(BaseModel):
    start_time: datetime
    end_time: datetime 
    


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    implement_crawl.delay('https://www.pinterest.com/ideas/')
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello from FastAPI!"})

# post, put api
# Khởi tạo basemodel để xác định đối tượng nhận được ở post và put
# Dùng các Path(), Query(), Body()

@app.get("/images", response_class=HTMLResponse)
async def postUrl(request: Request, page: int = 0, page_size: int = 20):
    images = image_services.get_offset_images(page=page, page_size=page_size)
    number_pages = image_services.get_pages(page_size)
    return templates.TemplateResponse("image.html", {
        "request": request,
        "images": images,
        "page": page,
        "page_size": page_size,
        "number_pages": number_pages
    })

@app.get("/api/images")
async def postUrl():
    list_images = image_services.get_all_images()
    return list_images

@app.get("/api/l_images")
async def limitUrl(page = 0, page_size = 20):
    list_images = image_services.get_offset_images(page=page, page_size=page_size)
    return list_images

@app.get("/api/number_pages")
async def number_pages(page_size = 20):
    number_pages = image_services.get_pages(page_size=page_size)
    return number_pages
    
# Lấy ra dữ liệu ảnh theo thời gian
@app.post("/api/image_for_time")
async def image_for_time(time_range: TimeRange):
    images_for_time = image_services.get_images_for_time(time_range.start_time, time_range.end_time)
    # urls_for_time = [image['url'] for image in images_for_time]
    return images_for_time

# ui
@app.get('/image_for_time', response_class=HTMLResponse)
async def image_for_time_ui(request: Request):
    return templates.TemplateResponse("time_image.html", {
        "request": request,     
    })
    

#download ảnh 
@app.post('/api/down_load_zip')
async def down_load_zip_api(time_range: TimeRange):
    images_for_time = image_services.get_images_for_time(time_range.start_time, time_range.end_time)
    url_for_time = [image['url'] for image in images_for_time]
    path_zip = get_image_services.download_and_zip_images(url_for_time, 'src/public', str(uuid4()))
    return f"http://localhost:8000/{path_zip}"

# ui
@app.get('/down_load_zip', response_class=HTMLResponse)
async def image_for_time_ui(request: Request):
    return templates.TemplateResponse("time_image_zip.html", {
        "request": request,     
    })
