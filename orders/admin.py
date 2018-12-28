from django.contrib import admin

from .models import Product, Account, Review, InCart, Inventory, Room
# Register your models here.
admin.site.register(Product)
admin.site.register(Account)
admin.site.register(InCart)
admin.site.register(Inventory)
admin.site.register(Room)