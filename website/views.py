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
    if(request.data["cart_count"] > 0):
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()
        
        context = {
            "total": request.data["total"],
            "cart_items": cart_items,
            "categories": request.data["categories"],
            "settings": request.data["settings"],
            "count": request.data["cart_count"]
        }
        
        return render(request, 'website/cart.html', context)
    else:
        messages.add_message(request, messages.ERROR, "Cart is empty!!")
        return redirect('website-home')

def add_to_cart(request, product_id):
    product = models.Product.objects.filter(id=product_id).first()
    cart = get_or_create_cart(request)
    
    cart_item, created = models.CartItem.objects.get_or_create(cart=cart, product=product, cost=product.cost, price=product.price)
    
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
    if(request.data["cart_count"] > 0):
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()
        
        context = {
            "total": request.data["total"],
            "cart_items": cart_items,
            "categories": request.data["categories"],
            "settings": request.data["settings"],
            "count": request.data["cart_count"]
        }
        
        return render(request, 'website/checkout.html', context)
    
    else:
        messages.add_message(request, messages.ERROR, "Cart is empty!!")
        return redirect('website-home')
    
def placeOrder(request):
    if request.method == "POST":
       cart = get_or_create_cart(request)
       
       first_name = request.POST.get('first_name')
       last_name = request.POST.get('last_name')
       email = request.POST.get('email')
       phone = request.POST.get('phone')
       country = request.POST.get('country')
       city = request.POST.get('city')
       state = request.POST.get('state')
       zip = request.POST.get('zip')
       address = request.POST.get('address')
       note = request.POST.get('note')
       order = models.Order.objects.create(cart_id=cart.id, first_name=first_name, last_name=last_name, email=email, phone=phone, country=country, city=city, state=state, zip=zip, note=note, address=address, total=request.data["total"])
       
       request.session.flush() #to delete session key from session
       
       messages.add_message(request, messages.SUCCESS, f"Your order has been placed! Order # {order.id}")
       return redirect('website-home')
       