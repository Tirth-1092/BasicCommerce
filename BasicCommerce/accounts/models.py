from django.contrib.auth.models import AbstractUser 
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    # phone_number = models.CharField(max_length=15, unique=True)
    phone_number = PhoneNumberField(blank=True, unique=True)


    def __str__(self):
        return self.username