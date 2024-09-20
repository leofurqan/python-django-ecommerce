from .models import Setting, Categories

class GeneralMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        data = {
            "categories": Categories.objects.all(),
            "settings": Setting.objects.first()
        }
        
        request.data = data
        response = self.get_response(request)
        return response