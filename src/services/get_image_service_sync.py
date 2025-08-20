import requests
import os
import logging
from typing import List
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import gevent

class GetImageSync():
    def __init__(self):
        pass

    def downImage(self, url : str, save_path):
        # Laays http request roi viet vao file
        filename = os.path.basename(urlparse(url).path)
        save_file_path = os.path.join(save_path, filename)
        try:
            response = requests.get(url)
            if (response.status_code == 200):
                
                try:
                    with open(save_file_path, "wb") as f:
                        f.write(response.content)
                except Exception as e:
                    logging.error(f"Lỗi không ghi được file ở url: {url}: {e}")
            else:
                logging.error(f"Lỗi request status ở url: {url}, status: {response.status_code}")

        except Exception as e:
            logging.error(f"request bị timeout: {e}")

    def downListImage(self, list_url : List[str], save_path: str):
        os.makedirs(save_path, exist_ok=True)
        # Dùng thread thật
        max_workers = min(4, len(list_url))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.downImage, url, save_path) for url in list_url]
            for f in futures:
                try:
                    f.result()
                except Exception as e:
                    logging.error(f"Lỗi tải ảnh {e}")

        #Thread của gevent thread ảo, tạo greenlet block đỡ hơn tí
        # jobs = [gevent.spawn(self.downImage, url, save_path) for url in list_url]
        # gevent.joinall(jobs)

getImageSync = GetImageSync()

        
        