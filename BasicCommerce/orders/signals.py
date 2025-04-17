# # orders/signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings

# from .models import Order  # if Order is defined in orders.models
# from payment.models import Payment  # import Payment from the payment app

# from catalog.models import Product  # Ensure this path matches your project structure

# @receiver(post_save, sender=Order)
# def order_confirmation_signal(sender, instance, created, **kwargs):
#     """
#     When a new order is created, update inventory for each order item and send an order confirmation email.
#     """
#     if created:
#         # Update inventory: for each order item, decrease the product's quantity.
#         for order_item in instance.items.all():
#             product = order_item.product
#             # Decrease inventory; prevent negative stock.
#             product.stock = max(0, product.stock - order_item.stock)
#             product.save(update_fields=['quantity'])
        
#         # Send order confirmation email
#         subject = f"Order #{instance.id} Confirmation"
#         message = (
#             f"Dear {instance.user.username},\n\n"
#             f"Thank you for your order. Your order has been confirmed and is now being processed."
#             f"\n Visit Again !"
#         )
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [instance.user.email]
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)


# @receiver(post_save, sender=Payment)
# def payment_status_signal(sender, instance, created, **kwargs):
#     """
#     When a payment instance is updated (i.e., not created), if the payment status is 'succeeded',
#     update the associated order's status and send a notification email.
#     """
#     # Only process updates, not initial creation.
#     if not created:
#         if instance.status == 'succeeded':
#             order = instance.order
#             # Update order status if it hasn't already been updated
#             if order.status != 'processing':
#                 order.status = 'processing'
#                 order.save(update_fields=['status'])
                
#                 # Send payment confirmation email
#                 subject = f"Payment Received for Order #{order.id}"
#                 message = (
#                     f"Dear {order.user.username},\n\n"
#                     f"We have received your payment for Order #{order.id}. Your order is now being processed."
#                 )
#                 from_email = settings.DEFAULT_FROM_EMAIL
#                 recipient_list = [order.user.email]
#                 send_mail(subject, message, from_email, recipient_list, fail_silently=False)


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Order  # Order model from your orders app
from payment.models import Payment  # Payment model from the payment app
from catalog.models import Product  # Adjust the import based on your project structure

@receiver(pre_save, sender=Order)
def order_status_update_signal(sender, instance, **kwargs):
    """
    Sends an email notification when the order status is updated.
    This signal compares the new status with the existing one.
    """
    if not instance.pk:
        # New Order instance; nothing to compare.
        return

    try:
        old_instance = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    # If the status has changed, send an update email.
    if old_instance.status != instance.status:
        subject = f"Order #{instance.pk} Status Updated"
        message = (
            f"Dear {instance.user.username},\n\n"
            f"Your order status has changed from '{old_instance.status}' "
            f"to '{instance.status}'.\n\nThank you for shopping with us."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=False)

@receiver(post_save, sender=Order)
def order_confirmation_signal(sender, instance, created, **kwargs):
    """
    When a new order is created, update the inventory for each order item and send
    an order confirmation email.
    """
    if created:
        # Update inventory for each order item.
        for order_item in instance.items.all():
            product = order_item.product
            # Decrease the product's stock; adjust field name if needed.
            product.stock = max(0, product.stock - order_item.quantity)
            product.save(update_fields=['stock'])
        
        # Send order confirmation email.
        subject = f"Order #{instance.id} Confirmation"
        message = (
            f"Dear {instance.user.username},\n\n"
            f"Your order has been confirmed with status '{instance.status}'.\n"
            "Thank you for your order and for shopping with us."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=False)

# @receiver(post_save, sender=Payment)
# def payment_status_signal(sender, instance, created, **kwargs):
#     """
#     When a Payment instance is updated (not created) and its status is 'succeeded',
#     update the associated order's status and send a notification email.
#     """
#     if not created and instance.status == 'succeeded':
#         order = instance.order
#         if order.status != 'processing':
#             order.status = 'processing'
#             order.save(update_fields=['status'])
            
#             subject = f"Payment Received for Order #{order.id}"
#             message = (
#                 f"Dear {order.user.username},\n\n"
#                 f"We have received your payment for Order #{order.id}.\n"
#                 "Your order is now being processed."
#             )
#             send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email], fail_silently=False)
