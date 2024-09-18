from django.shortcuts import render

def index(request):
    return render(request, 'website/index.html')

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