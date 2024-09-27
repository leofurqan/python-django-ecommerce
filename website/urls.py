from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='website-home'),
    path('shop', views.shop, name='website-shop'),
    path('shop/<int:category_id>/', views.shop_category, name='website-shop-category'),
    path('shop/search/', views.shop_search, name='search-products'),
    path('detail/<int:id>/', views.detail, name='website-detail'),
    path('about', views.about, name='website-about'),
    path('blogs', views.blogs, name='website-blogs'),
    path('contact', views.contact, name='website-contact'),
    path('cart', views.cart, name='website-cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('checkout', views.checkout, name='website-checkout'),
    path('placeOrder', views.placeOrder, name='website-place-order'),
]
