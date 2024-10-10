from django.shortcuts import render, redirect
from . import models
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import CategoriesSerializer
from rest_framework.permissions import IsAuthenticated
from django.template import loader
from django.core.mail import send_mail
from django.http import HttpResponse

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
    quantity = int(request.POST.get("quantity", 1))
    
    cart_item, created = models.CartItem.objects.get_or_create(cart=cart, product=product, cost=product.cost, price=product.price, total=quantity*product.price)
    
    if not created:
        cart_item.quantity += quantity
        cart_item.total = cart_item.quantity * cart_item.price
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    messages.add_message(request, messages.SUCCESS, "Product added to Cart")
    return redirect('website-home')

def delete_cart_item(request, item_id):
    cart_item = models.CartItem.objects.filter(id=item_id).first()
    cart_item.delete()
    
    messages.add_message(request, messages.SUCCESS, "Cart Item Deleted Successfully...")
    return redirect('website-cart')

def update_cart(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist("cart_item_ids")
        quantities = request.POST.getlist("quantities")
        
        for item_id, quantity in zip(item_ids, quantities):
            quantity = int(quantity)
            if quantity > 0:
                cart_item = models.CartItem.objects.filter(id=item_id).first()
                cart_item.quantity = quantity
                cart_item.total = quantity * cart_item.price
                cart_item.save()
            else:
                models.CartItem.objects.filter(id=item_id).delete()
        messages.add_message(request, messages.SUCCESS, "Cart updated successfully...")
                
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
       cart_items = cart.items.all()
       
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
       
       context = {
            "order": order,
            "cart_items": cart_items,
            "settings": request.data["settings"],
        }
       
       subject = "Order Confirmation"
       message = loader.render_to_string('website/mail/order_confirmation.html', context)
       send_mail(subject, message, "leofurqan12@gmail.com", [email], html_message=message)
       
       request.session.flush() #to delete session key from session
       
       messages.add_message(request, messages.SUCCESS, f"Your order has been placed! Order # {order.id}")
       return redirect('website-home')
    
# API Calls
#API's

class CategoriesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        categories = models.Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)   

class CategoriesDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, category_id):
        try:
            category = models.Categories.objects.get(id=category_id)
            serializer = CategoriesSerializer(category)
            return Response(serializer.data)
        except models.Categories.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
    
    def put(self, request, category_id):
        try:
            category = models.Categories.objects.get(id=category_id)
            serializer = CategoriesSerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        except models.Categories.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        
    def delete(self, request, category_id):
        try:
            category = models.Categories.objects.get(id=category_id)
            category.delete()
            return Response({'message': 'Category deleted successfully'}, status=204)
        except models.Categories.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404) 