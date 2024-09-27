from .models import Setting, Categories, Cart
from django.http import HttpResponse;
from django.shortcuts import get_object_or_404;

class GeneralMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        session_key = request.session.session_key
        if not session_key:
            count = 0
        else:
            cart = Cart.objects.filter(session_key=session_key).first()
            count = cart.items.count()
            
        data = {
            "categories": Categories.objects.all(),
            "settings": Setting.objects.first(),
            "cart_count": count
        }

        request.data = data
        response = self.get_response(request)
        return response