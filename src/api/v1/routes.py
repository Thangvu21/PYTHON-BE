from fastapi import APIRouter
from src.api.v1.endpoint.Image import router as ImageRouter
from src.api.v1.endpoint.Down import router as DownRouter

routers = APIRouter()
router_list = [ImageRouter, DownRouter]

for router in router_list:
    routers.include_router(router, tags=["v1"])