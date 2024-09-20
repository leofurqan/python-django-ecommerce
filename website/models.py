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