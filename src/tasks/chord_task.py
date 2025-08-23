from celery import shared_task, chord, group
from datetime import datetime
from src.services.get_images import get_image_services
from src.services.image_services import image_services
import logging
import os
import shutil
from typing import List, Tuple
from celery.result import GroupResult
import asyncio_gevent, asyncio
from asgiref.sync import async_to_sync

# nhận vào 1 batch tuple url dir 
@shared_task(name="create_list_image_v2", bind=True)
def create_list_image(self, url_save_path_list: List[Tuple[str, str]]):
    url_list = [url[0] for url in url_save_path_list]
    if not url_save_path_list:
        return
    save_path = url_save_path_list[0][1]

    try:
        # Bước 3: Gọi hàm đã bọc để thực thi và chờ kết quả.
        # Bị lỗi không có
        # pool = asyncio.get_event_loop()
        # result = pool.run_until_complete(get_image_services.downListImages(url_list, save_path))
        # asyncio.run(): bị lỗi có rồi:))
        # ra sản phẩm nhưng báo lỗi chỉ được 33 / 47 thôi
        # You cannot use AsyncToSync in the same thread as an async event loop - just await the async function directly.
        # result = async_to_sync(get_image_services.downListImages)(url_list, save_path)
        # Vì thằng chord nó chỉ quản lý việc evevt driven rồi nên việc quản lý bất đồng bộ cho trong task thì không được
        # viết chord khác

        # You cannot use AsyncToSync in the same thread as an async event loop - just await the async function directly.
        # result = async_to_sync(
        #     get_image_services.downListImages)(url_list, save_path)

        # result = async_to_sync(get_image_services.downListImages)(url_list, save_path)
        os.makedirs(save_path, exist_ok=True)

        try:
            # Không dùng lặp từng cái nữa mà xử lý theo batch
            
            # return exceptions sẽ dừng lại ngay lập tức khi raise exception
            # Tất cả các task con đều được chạy đến cùng, dù có task nào đó bị lỗi.
            loop = asyncio.get_event_loop()
            group = asyncio.gather(*[get_image_services.downImage(save_path=save_path, url=url) for url in url_list], 
                                   return_exceptions=True)
            result = loop.run_until_complete(group)
            loop.close()
        except Exception as e:
            print(f'Lỗi khi tải về nhiều ảnh: {e}')


        return f"done:{result}"
    except Exception as e:
        logging.error(f"Task ID {self.request.id}: Lỗi khi ghi nhiều ảnh: {e}", exc_info=True)

#Tạo zip và xóa folder ảnh
@shared_task(name="zip_v2", bind = True)
def create_folder_zip(self, groups, save_path: str):

    temp_dir = os.path.abspath(save_path)
    try:
        # tại đây thì mình tạo zip và xóa folder đi
        # Tại vì tạo ra zip là trả về id như mình tạo ra task trả về id luôn
        # Nên nó là hàm bất đồng bộ
        zip_path = shutil.make_archive(
                save_path,
                "zip",
                temp_dir
            )
        
        logging.info(f"Task ID {self.request.id}: Tạo file zip thành công: {zip_path}")


        try:
            shutil.rmtree(temp_dir)
            logging.info(f"Task ID {self.request.id}: Đã xóa thư mục tạm: {temp_dir}")
        except Exception as e:
            logging.error(f"Lỗi xóa thư mục tạm: {e}")
            logging.error(f"Task ID {self.request.id}: Lỗi khi xóa thư mục tạm '{temp_dir}': {e}", exc_info=True)
        
        return zip_path
    except Exception as e:
        logging.error(f"Task ID {self.request.id}: Lỗi tạo file zip cho thư mục '{temp_dir}': {e}", exc_info=True)

    # Lỗi trả về trong khối đầu tiên không trả veed đúng giá trị nên nó trả về tuple ảo 

@shared_task(name="check-process", bind = True)
def process(self, group_id, save_path: str):
    group_result = GroupResult.restore(group_id)

    if group_result:
        
        logging.info(f"group task đã hoàn thành {group_id}")
    
        if group_result.successful():
            logging.info(f"group task đã thành công và sẵn sàng zip: {group_id}")


            try:
                zip = create_folder_zip.delay(save_path)
                logging.info(f"Bắt đầu tạo zip, task_id: {self.request.id}")
                return zip.request.id

            except Exception as e:
                logging.error(f"Lỗi tạo zip ở task: {self.request.id}: {e}")
        else:
            logging.info(f"group task đã thất bại")
    else:
        logging.info(f"Task group chưa hoàn thành tại: {group_id}")
        self.retry(countdown = 1, max_retries = 2)

@shared_task(name="pipeline_v2", bind= True)
def pipeline_v2(self, start_time: datetime, end_time: datetime, save_dir: str, zip_name: str):

    logging.info(f"Task {self.request.id}: đang được chạy")

    save_path = os.path.join(save_dir, zip_name)

    # Lấy ra db đã tạo signature không gọi thẳng task để giảm overhead
    # có nghĩa là nó tính giá trị tham số trước khi thực hiện hàm nên truyền kiểu này
    try:
        urls = image_services.get_images_for_time(start_time, end_time)
        # logging.info(f" data lấy về : {urls}")
    except Exception as e:
        logging.error(f"Task ID {self.request.id}: Lỗi khi truy vấn DB: {e}", exc_info=True)

    if len(urls) == 0:
        logging.warning("không có url nào trong khoảng thời gian này")
        return None

    url_save_path_list = [(url['url'], save_path) for url in urls]

    batch_size = 30
    tasks = []

    for i in range(0, len(urls), batch_size):
        chunk = url_save_path_list[i: i + batch_size]
        res = create_list_image.s(chunk)
        tasks.append(res)


    # Chờ tất cả task con hoàn thành (có thể dùng AsyncResult)
    header = group(tasks)

    # Sau khi tất cả task con xong, tạo zip
    pipe = chord(header=header)(create_folder_zip.s(save_path))
    final_result = pipe.get()  
    return final_result
