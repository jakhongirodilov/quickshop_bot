from django.contrib import admin
from .models import Category, Subcategory, Users, Product, Cart, Order

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Users)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
