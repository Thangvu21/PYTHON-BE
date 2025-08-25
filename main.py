from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.tasks.crawl_image_tasks import implement_crawl
import asyncio
from src.core.celery import celery
from src.services.get_image_service_sync import getImageSync
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from src.api.v1.routes import routers
from src.api.v1.endpoint.Down import image_services
from src.config.broker import r
from src.config.conf import config_server

templates = Jinja2Templates(directory="src/templates")

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
app.include_router(routers, prefix="/api")

#ui
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Thử đợi 1 s để nó khởi tạo celery xong xem sao
    await asyncio.sleep(1)
    implement_crawl.delay('https://www.pinterest.com/ideas/')
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello from FastAPI!"})

@app.get("/images", response_class=HTMLResponse)
async def postUrl(request: Request, page: int = 0, page_size: int = 20):
    # images = image_services.get_offset_images(page=page, page_size=page_size)
    images= await run_in_threadpool(
        image_services.get_offset_images,
        page,
        page_size
    )
    # number_pages = image_services.get_pages(page_size)
    number_pages = await run_in_threadpool(
        image_services.get_pages,
        page_size
    )
    return templates.TemplateResponse("image.html", {
        "request": request,
        "images": images,
        "page": page,
        "page_size": page_size,
        "number_pages": number_pages,
        "current_page": page,
        "number_pages": number_pages
    })

    
@app.get('/image_for_time', response_class=HTMLResponse)
def image_for_time_ui(request: Request):
    return templates.TemplateResponse("time_image.html", {
        "request": request,     
    })

@app.get('/down_load_zip', response_class=HTMLResponse)
def image_for_time_ui(request: Request):
    return templates.TemplateResponse("time_image_zip.html", {
        "request": request,     
    })
