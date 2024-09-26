from django.shortcuts import render, redirect
from . import models
from django.http import HttpResponse
from django.contrib import messages

def index(request):
    featured_products = models.Product.objects.filter(is_featured=True, status=True)
    trending_products = models.Product.objects.filter(is_trending=True, status=True)
    context = {
        "featured": featured_products,
        "trending": trending_products,
        "categories": request.data["categories"],
        "settings": request.data["settings"],
        "count": request.data["cart_count"]
    }
    
    return render(request, 'website/index.html', context)

def shop(request):
    products = models.Product.objects.filter(status=True)
    
    context = {
        "products": products,
        "categories": request.data["categories"],
        "settings": request.data["settings"],
        "count": request.data["cart_count"]
    }
    return render(request, 'website/shop.html', context)

def shop_category(request, category_id):
    products = models.Product.objects.filter(category_id=category_id, status=True)
    
    context = {
        "products": products,
        "categories": request.data["categories"],
        "settings": request.data["settings"],
        "count": request.data["cart_count"]
    }
    return render(request, 'website/shop.html', context)

def shop_search(request):
    query = request.GET.get('search')
    products = models.Product.objects.filter(name__icontains=query, status=True)
    
    context = {
        "products": products,
        "categories": request.data["categories"],
        "settings": request.data["settings"],
        "count": request.data["cart_count"]
    }
    return render(request, 'website/shop.html', context)

def detail(request, id):
    product = models.Product.objects.filter(id=id).first()
    related_products = models.Categories.objects.get(id=product.category_id).products.all()
    
    context = {
        "product": product,
        "related_products": related_products,
        "categories": request.data["categories"],
        "settings": request.data["settings"],
        "count": request.data["cart_count"]
    }
    
    return render(request, 'website/detail.html', context)

def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')

def blogs(request):
    return render(request, 'website/blogs.html')

def get_or_create_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    cart, created = models.Cart.objects.get_or_create(session_key=session_key)

    return cart

def cart(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if(request.data["cart_count"] > 0):
        context = {
            "total": total,
            "cart_items": cart_items,
            "categories": request.data["categories"],
            "settings": request.data["settings"],
            "count": request.data["cart_count"]
        }
        
        total = 0
        for item in cart_items:
            total += models.CartItem.get_total_price(item)
        
        return render(request, 'website/cart.html', context)
    else:
        messages.add_message(request, messages.ERROR, "Cart is empty!!")
        return redirect('website-home')

def add_to_cart(request, product_id):
    product = models.Product.objects.filter(id=product_id).first()
    cart = get_or_create_cart(request)
    
    cart_item, created = models.CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.add_message(request, messages.SUCCESS, "Product added to Cart")
    return redirect('website-home')

def delete_cart_item(request, item_id):
    cart_item = models.CartItem.objects.filter(id=item_id).first()
    cart_item.delete()
    
    messages.add_message(request, messages.SUCCESS, "Cart Item Deleted Successfully...")
    return redirect('website-cart')

def checkout(request):
    return render(request, 'website/checkout.html')