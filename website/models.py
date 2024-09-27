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
    
class Cart(models.Model):
    session_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart #{self.id}, {self.session_key}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} in Cart #{self.cart.id}"
    
    def get_total_price(self):
        return self.quantity * self.product.price
    
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="orders")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.TextField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    note = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, default="pending")
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id}"
    