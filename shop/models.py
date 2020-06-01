

from django.conf import settings
import uuid
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField



# Create your models here.

ACCOUNT = (
    ('Customer', 'Customer'),
    ('Farmer', 'Farmer'),
)

CATEGORY_CHOICES = (
    ('Cows', 'Cows'),
    ('Chicken', 'Chicken'),
    ('Goats', 'Goats'),
    ('Ducks', 'Ducks'),
    ('Sheep', 'Sheep'),
    ('Rabits', 'Rabits'),
    ('Pigs', 'Pigs')
    
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField( max_length=8,
                             choices=ACCOUNT,
                             default='Customer')

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    #label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    image = models.FileField()
    ratings = GenericRelation(Rating, related_query_name='queryset')
    saler = models.ForeignKey(
        'Farmer', related_name='saler', on_delete=models.SET_NULL, blank=True, null=True)
    #ratings feild


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product", args=[str(self.pk)
        ])

    def get_add_to_cart_url(self):
        return reverse("shop:add_to_cart", args=[str(self.pk)])

    def get_remove_from_cart_url(self):
        return reverse("shop:remove_from_cart", args=[str(self.pk)])
    
    def get_farm_url(self):
        return reverse("shop:farmDetailView", args=[str(self.saler)])
    
    def get_category_url(self):
        return reverse("shop:categoryView", args=[str(self.category)])
class Rate(models.Model):
    name = models.CharField(max_length = 140)
    ratings =  GenericRelation(Rating, related_query_name= 'object_list')

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    saler = models.ForeignKey(
        'Farmer',on_delete=models.SET_NULL, blank=True, null=True)
    
    


    def __str__(self):
        return f'{self.quantity} of {self.item.title} for {self.item.saler}'
    

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem )
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    saler = models.ForeignKey(
        'Farmer',on_delete=models.SET_NULL, blank=True, null=True)
    
        

    def __str__(self):
        return self.user.username 

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
    def get_number(self):
        number = 0
        for order_item in self.items.all():
            number += order_item.count()
        return number
    def orders_of_farmer(self):
        return f'{self.quantity} of {self.item.title} for {self.item.saler}'

class OrderItem2(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    saler = models.ForeignKey(
        'Farmer',on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.title} for {self.item.saler}'
    

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Farmer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,default=1)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length = 100)
    email = models.EmailField(default = None)
    farmname = models.CharField(max_length = 50)
    farmlocation = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 10)

    #orders
    

    def __str__(self):
        return self.farmname

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=100)
    shipping_village = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    customer_phone = models.CharField(max_length=100)
    customer_mobilemoneyphone = models.CharField(max_length=100)
    shipping_notes = models.CharField(max_length=150)
    payment_option = models.CharField(max_length=10) 
    

    def __str__(self):
        return self.user.username