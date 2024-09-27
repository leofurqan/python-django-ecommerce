from django.contrib import admin
from . import models

class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 0

admin.site.register(models.Setting)
admin.site.register(models.Categories)
admin.site.register(models.Product)

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key')
    inlines = [CartItemInline]

admin.site.register(models.CartItem)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('cart', 'first_name', 'last_name', 'total')
    inlines = []
    
    def show_cart_items(self, obj):
        items = obj.cart.cart_items.all()
        return ', '.join(f"{item.product.name} (x{item.quantity})" for item in items)

    show_cart_items.short_description = 'Cart Items'

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('cart', 'total')
    inlines = []  # You can keep this empty since we'll use a method instead
