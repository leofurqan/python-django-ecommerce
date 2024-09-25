from django.contrib import admin
from . import models

admin.site.register(models.Setting)
admin.site.register(models.Categories)
admin.site.register(models.Product)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
