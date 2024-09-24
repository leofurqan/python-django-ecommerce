from django.db import models

class Setting(models.Model):
    site_title = models.CharField(max_length=100)
    system_name = models.CharField(max_length=100)
    site_logo = models.ImageField(upload_to="")
    favicon = models.FileField(upload_to="")
    home_banner = models.ImageField(upload_to="")
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.TextField()
    facebook = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    footer_text = models.TextField()
    
class Categories(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="categories/")
    description = models.TextField()
    status = models.BooleanField()
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    short_desc = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    is_trending = models.BooleanField()
    is_featured = models.BooleanField()
    status = models.BooleanField()
    
    def __str__(self):
        return self.name