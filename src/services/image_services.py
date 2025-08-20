from typing import List
from src.db.db import engine
from src.db.model import Image
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import and_


class ImageModel():
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def add_image(self, image: Image):
        with self.Session() as session:
            try:
                session.add(image)
                session.commit()
                return {"status": "Success khi thêm ảnh", "id": image.id}
            except Exception as e:
                session.rollback()
                return {"status": f"Error khi thêm ảnh {e}"}
        
    def add_images(self, images: List[Image]):
        with self.Session() as session:
            try:
                for image in images:
                    session.add(image)
                session.commit()
                return {"status": "Success khi thêm nhiều ảnh"}
            except Exception as e:
                session.rollback()
                return {"status": f"Error khi thêm nhiều ảnh: {e}"}
    
    def delete_image(self, id: str):
        with self.Session() as session:
            try:
                image_deleted = session.get(Image, id)
                if not image_deleted:
                    return {"status": "Image không tồn tại"}
                session.delete(image_deleted)
                session.commit()
                return {"status": "Success khi xóa ảnh"}
            except Exception as e:
                session.rollback()
                return {"status": f"Error khi xóa ảnh: {e}"}
     
    def update_image(self, id: str, image: Image):
        with self.Session() as session:
            try:
                image_updated = session.get(Image, id)
                if not image_updated:
                    return {"status": "Image không tồn tại"}
                
                image_updated.url = image.url
                session.commit()
                return {"status": "Image cập nhật thành công"}
            except Exception as e:
                session.rollback()
                return {"status": f"Error khi cập nhật ảnh: {e}"}
    
    def get_image(self, id: str):
        with self.Session() as session:
            try:
                image = session.query(Image).filter(Image.id == id).first()
                if not image:
                    return {"status": "Image không tồn tại"}
                
                return {
                        "id": image.id,
                        "url": image.url,
                        "time_saved": image.time_saved  }
            except Exception as e:
                return {"status": f"Error khi tìm ảnh: {e}"}   
        
    def get_all_images(self):
        with self.Session() as session:
            try:
                images = session.query(Image).all()
                images_object = []
                for image in images:
                    images_object.append(
                        {
                            "id": image.id,
                            "url": image.url,
                            "time_saved": image.time_saved
                        }
                    )
                return images_object

            except Exception as e:
                return {"status": f"Error khi tìm tất cả ảnh: {e}"}
            
    # all xong mới làm filter theo thời gian
    def get_offset_images(self, page: int = 0, page_size = None):
        with self.Session() as session:
            try:
                query = session.query(Image)
                if page_size is not None:
                    query = query.limit(page_size)
                    if page:
                        print(f"page: {page}, limit = {page_size}, offset = {int(page_size) * int(page)}")
                        # Ép kiểu không ra lỗi
                        query = query.offset((int(page_size) - 1) * int(page))
                image_objects = []
                images = query.all()
                for image in images:
                    image_objects.append(
                        {
                            "id": image.id,
                            "url": image.url,
                            "time_saved": image.time_saved
                        }
                    )
                return image_objects
            except Exception as e:
                return {"status": f"Error khi tìm tất cả ảnh với limit và offset: {e}"}
    
    def get_pages(self, page_size = None):
        with self.Session() as session:
            try:
                query = session.query(Image)

                number_images = query.count()
                
                if page_size:
                    number_pages = number_images / int(page_size) + 1
                    return int(number_pages)
            except Exception as e:
                return {"status": f"Error khi tìm độ số trang với limit và offset: {e}"}

    def get_images_for_time(self, start_time: datetime, end_time: datetime):
        with self.Session() as session:
            try:
                query = session.query(Image).filter(
                    and_(
                        Image.time_saved > start_time,
                        Image.time_saved < end_time
                    )
                )       
                image_objects = []
                images = query.all()
                for image in images:
                    obj: dict = {
                            "id": image.id,
                            "url": image.url,
                            "time_saved": image.time_saved
                        }
                    image_objects.append(
                        obj
                    )
                return image_objects         
            except Exception as e:
                return {"status": f"Error khi tìm tất cả ảnh theo thời gian: {e}"}

image_services = ImageModel()

    

