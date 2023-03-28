from django.contrib import admin
from ecomapp.models import Customer, Products, Cart, RentedItems 

# Register your models here.

admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(RentedItems)