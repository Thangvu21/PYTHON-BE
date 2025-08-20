from locust import HttpUser, task, between

class ImageUser(HttpUser):
    host = "http://localhost:8000"  # Địa chỉ FastAPI server của bạn
    wait_time = between(1, 2)  # Mỗi user ảo chờ 1–2 giây giữa các request

    @task
    def get_images(self):
        self.client.post(
            url="/api/down/chord_image_gevent",
            json={
                "start_time": "2025-07-28T00:00:00",
                "end_time": "2025-08-01T00:00:00"
            }
        )