from django.db import models
from django.conf import settings
from orders.models import Order  # Link to orders app

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('requires_action', 'Requires Action')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stripe_payment_id = models.CharField(max_length=100, null=True, blank=True)
    hosted_invoice_url = models.URLField(null=True, blank=True)  # New field for receipt
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.status}"


class PaymentIntent(models.Model):
    INTENT_STATUS_CHOICES = [
        ('requires_payment_method', 'Requires Payment Method'),
        ('requires_confirmation', 'Requires Confirmation'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        # Add additional choices if needed
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    stripe_intent_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, choices=INTENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Optional, if you want to track updates
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment Intent"
        verbose_name_plural = "Payment Intents"
    
    def __str__(self):
        return f"PaymentIntent {self.stripe_intent_id} for Payment #{self.payment.id}"
    

    