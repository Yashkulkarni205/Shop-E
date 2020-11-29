from django.contrib import admin
from .models import Contact, Product, ProductImage, UserDetail, Order

# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(UserDetail)
admin.site.register(Order)
