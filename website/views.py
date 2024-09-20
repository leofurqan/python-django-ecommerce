from django.shortcuts import render
from . import models
from django.http import HttpResponse

def index(request):
    context = {
        "categories": request.data["categories"],
        "settings": request.data["settings"]
    }
    
    return render(request, 'website/index.html', context)

def shop(request):
    return render(request, 'website/shop.html')

def detail(request):
    return render(request, 'website/detail.html')

def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')

def blogs(request):
    return render(request, 'website/blogs.html')

def cart(request):
    return render(request, 'website/cart.html')

def checkout(request):
    return render(request, 'website/checkout.html')