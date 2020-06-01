from django.contrib import admin

# Register your models here.
from .models import Item, OrderItem, Order,Farmer,Address,UserProfile,OrderItem2


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Farmer)
admin.site.register(Address)
admin.site.register(UserProfile)
admin.site.register(OrderItem2)