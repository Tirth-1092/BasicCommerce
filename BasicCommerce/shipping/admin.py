from django.contrib import admin
from .models import ShippingAddress,ShippingMethod,DeliveryStatus

admin.site.register(ShippingAddress)
admin.site.register(ShippingMethod)
admin.site.register(DeliveryStatus)