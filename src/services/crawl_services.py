import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from ..config.conf import Configuration

class CrawlImageService():
    def __init__(self, url):
        self.page_url = url
    
    def crawl(self):
        try:
            page = requests.get(self.page_url,                         
                params={
                    'query': 'cats',
                    'per_page': 10
                },
                headers={
                    "Authorization": Configuration().key_pexels  
                })
            # kiểm tra trạng thái 403/500
            page.raise_for_status()
        except requests.RequestException as e:
            print(f"Lỗi khi crawl {e}")
            return []
        soup = BeautifulSoup(page.text, 'html.parser')
        wrapper = soup.find('body')

        if wrapper is None:
            print("Không tìm thấy thẻ <body> trong trang.")
            return []

        image_urls = wrapper.find_all('img')
        return [
        url['src'] for url in image_urls
        if self.is_real_image_url(url['src']) == True
    ]

    def is_real_image_url(self, url: str) -> bool:
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.svg')
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()

        return path.endswith(image_extensions) and not url.startswith('data:')


    

# page14 = CrawlImageService('https://www.pinterest.com/ideas/')

# print(page14.crawl())