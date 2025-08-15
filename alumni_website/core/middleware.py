import psutil
import os

class SimpleResourceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            cpu_percent = process.cpu_percent()
            print(f"🔍 {request.path}: Memory={memory_mb:.1f}MB CPU={cpu_percent:.1f}%")
        except:
            pass
            
        response = self.get_response(request)
        return response