from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(default='default_img.png',upload_to='products_pics')
    price = models.DecimalField(max_digits=7, decimal_places=3)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    in_stock = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        super().save()
        img = Image.open(self.thumbnail.path)
        if img.height > 394 or img.width > 394:
            output_size = (394, 394)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    def __str__(self):
	    return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.id 
    @property
    def get_cart_total(self):
        orderitems = self.orderproduct_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderproduct_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    def __str__(self)->str:
        return  self.product.name