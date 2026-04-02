from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # Giả lập người dùng thật: đọc nội dung trang từ 1 đến 3 giây rồi mới click tiếp
    wait_time = between(1.0, 3.0)

    @task(4)
    def call_light_api(self):
        # Xác suất 80% người dùng sẽ gọi tác vụ nhẹ
        self.client.get("/light")

    @task(1)
    def call_heavy_api(self):
        # Xác suất 20% người dùng sẽ gọi tác vụ nặng (cái này sẽ làm server đuối sức)
        self.client.get("/heavy")