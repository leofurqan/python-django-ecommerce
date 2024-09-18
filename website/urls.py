from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='website-home'),
    path('shop', views.shop, name='website-shop'),
    path('detail', views.detail, name='website-detail'),
    path('about', views.about, name='website-about'),
    path('blogs', views.blogs, name='website-blogs'),
    path('contact', views.contact, name='website-contact'),
    path('cart', views.cart, name='website-cart'),
    path('checkout', views.checkout, name='website-checkout'),
]
