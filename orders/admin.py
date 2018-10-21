from django.contrib import admin

from .models import Product, User, Review
# Register your models here.
admin.site.register(Product)
admin.site.register(User)