import requests
from typing import List
import os
from urllib.parse import urlparse
import shutil

class GetImageService():
    def __init__(self):
        pass

    def downImage(self, url: str, save_path: str):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"Ảnh đã được ghi thành công: {url}", save_path)
            else:
                print(f"Ảnh đã được ghi thất bại Mã trạng thái: {response.status_code}")

        except Exception as e:
            print(f"Lỗi {e}")

    def downListImages(self, list_url: List[str], save_dir: str):
        os.makedirs(save_dir, exist_ok=True)

        try:
            for idx, url in enumerate(list_url):
                save_path = self.build_path(save_dir, url)
                self.downImage(url, save_path)
            
        except Exception as e:
            print(f'Lỗi khi tải về nhiều ảnh: {e}')
    
    def build_path(self, save_dir, url):
        filename = os.path.basename(urlparse(url).path)
        save_path = os.path.join(save_dir, filename)
        return save_path
    
    def download_and_zip_images(self, list_url: List[str], save_dir: str, zip_name: str):
        save_dir = os.path.join(save_dir, zip_name)
        self.downListImages(list_url, save_dir)
        zip_path = shutil.make_archive(os.path.join(os.path.dirname(save_dir), zip_name), 'zip', save_dir)
        # xóa luôn thư mục chứa ảnh tiết kiệm bộ nhớ
        shutil.rmtree(save_dir)
        # lúc nãy điền nhầm zip_path nên noskhoong tìm thấy:)) bây giờ tải được rồi
        zip_filename = os.path.basename(zip_path)
        return f"public/{zip_filename}"

serviceImage = GetImageService()

url = ['https://kenh14cdn.com/zoom/220_289/203336854389633024/2025/7/31/mingahaman3464186873596599076s2025-7-31-1338162-story-1753943917179628354607-1753945493691-17539454938822117163387-0-76-1800-1426-crop-1753945537782723595179.jpg'
,
'https://kenh14cdn.com/zoom/250_156/203336854389633024/2025/7/31/avatar1753945864474-1753945864815812073403-0-119-268-548-crop-17539458846711089978277.jpeg'
]
save_dir = 'public'

# save_path = serviceImage.build_path(save_dir, url)

# parsed: ParseResult(scheme='https', 
#                     netloc='kenh14cdn.com', 
#                     path='/zoom/250_156/203336854389633024/2025/7/31/avatar1753945864474-1753945864815812073403-0-119-268-548-crop-17539458846711089978277.jpeg', 
#                     params='', 
#                     query='', 
#                     fragment='')

# Chắc phải tạo xong xóa luôn file đó
# print(serviceImage.download_and_zip_images(url, save_dir, '2'))