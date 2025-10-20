from django.contrib import admin
from EkartApp.models import Category,Product,Cart,Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)