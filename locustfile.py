try:
    from locust import HttpUser, task, between
except ImportError:
    class HttpUser:
        wait_time = None
    def task(weight=1):
        def decorator(fn):
            return fn
        return decorator
    def between(a, b):
        return None

class WebsiteUser(HttpUser):
    wait_time = between(1.0, 3.0)

    @task(4)
    def call_light_api(self):
        self.client.get("/light")

    @task(1)
    def call_heavy_api(self):
        self.client.get("/heavy")