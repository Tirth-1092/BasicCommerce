# from django.db import models
# from django.conf import settings
# from django.core.validators import MinValueValidator
# from django.utils import timezone

# class Coupon(models.Model):
#     DISCOUNT_TYPES = (
#         ('percentage', 'Percentage'),
#         ('fixed', 'Fixed Amount'),
#     )

#     code = models.CharField(max_length=50, unique=True)
#     discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     max_usage = models.PositiveIntegerField(default=1)
#     used_count = models.PositiveIntegerField(default=0)
#     active = models.BooleanField(default=True)
#     min_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CouponUsage')

#     def is_valid(self, user, cart_total):
#         now = timezone.now()
#         return (
#             self.active and
#             self.valid_from <= now <= self.valid_to and
#             self.used_count < self.max_usage and
#             cart_total >= self.min_cart_value and
#             not self.couponusage_set.filter(user=user).exists()
#         )

#     def __str__(self):
#         return self.code

# class CouponUsage(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
#     used_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'coupon')

# class Discount(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     discount_type = models.CharField(max_length=10, choices=Coupon.DISCOUNT_TYPES)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     applicable_to = models.CharField(max_length=20, choices=[('all', 'All Products'), ('category', 'Category')])
#     category = models.ForeignKey('catalog.Category', null=True, blank=True, on_delete=models.SET_NULL)
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone

class Coupon(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_usage = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    min_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CouponUsage')

    def is_valid(self, user, cart_total):
        now = timezone.now()
        return (
            self.active and
            self.valid_from <= now <= self.valid_to and
            self.used_count < self.max_usage and
            cart_total >= self.min_cart_value and
            not self.couponusage_set.filter(user=user).exists()
        )

    def __str__(self):
        return self.code

class CouponUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'coupon')

class Discount(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount_type = models.CharField(max_length=10, choices=Coupon.DISCOUNT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    applicable_to = models.CharField(max_length=20, choices=[('all', 'All Products'), ('category', 'Category')])
    category = models.ForeignKey('catalog.Category', null=True, blank=True, on_delete=models.SET_NULL)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
