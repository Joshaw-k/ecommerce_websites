from django.contrib import admin
from .models import Product,Order,OrderItem,Shipping_Address

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Shipping_Address)
