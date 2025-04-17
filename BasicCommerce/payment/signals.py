from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Payment  # Payment model from the payment app

@receiver(post_save, sender=Payment)
def payment_status_signal(sender, instance, created, **kwargs):
    """
    When a Payment instance is updated (not created) and its status is 'succeeded',
    update the associated order's status and send a notification email.
    """
    if not created and instance.status == 'succeeded':
        order = instance.order
        if order.status != 'processing':
            order.status = 'processing'
            order.save(update_fields=['status'])
            
            subject = f"Payment Received for Order #{order.id}"
            message = (
                f"Dear {order.user.username},\n\n"
                f"We have received your payment for Order #{order.id}.\n"
                "Your order is now being processed."
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email], fail_silently=False)
