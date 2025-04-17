from django.contrib import admin
from .models import Coupon,CouponUsage,Discount

admin.site.register(Coupon)
admin.site.register(CouponUsage)
admin.site.register(Discount)