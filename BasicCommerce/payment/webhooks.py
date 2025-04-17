# # from django.http import HttpResponse
# # from django.views.decorators.csrf import csrf_exempt
# # from django.conf import settings
# # import stripe
# # import json

# # # Import your Payment model
# # from .models import Payment

# # stripe.api_key = settings.STRIPE_SECRET_KEY

# # @csrf_exempt
# # def stripe_webhook(request):
# #     payload = request.body
# #     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
# #     try:
# #         event = stripe.Webhook.construct_event(
# #             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
# #         )
# #     except ValueError as e:
# #         # Invalid payload
# #         return HttpResponse(status=400)
# #     except stripe.error.SignatureVerificationError as e:
# #         # Invalid signature
# #         return HttpResponse(status=400)

# #     # Handle payment intent events
# #     if event['type'] == 'payment_intent.succeeded':
# #         payment_intent = event['data']['object']
# #         handle_payment_success(payment_intent)
# #     elif event['type'] == 'payment_intent.payment_failed':
# #         payment_intent = event['data']['object']
# #         handle_payment_failure(payment_intent)

# #     return HttpResponse(status=200)

# # def handle_payment_success(payment_intent):
# #     try:
# #         payment = Payment.objects.get(stripe_payment_id=payment_intent['id'])
# #         payment.status = 'succeeded'
# #         payment.save()
# #         # Add any additional order fulfillment logic here if needed.
# #     except Payment.DoesNotExist:
# #         # Log the error if necessary.
# #         pass

# # def handle_payment_failure(payment_intent):
# #     try:
# #         payment = Payment.objects.get(stripe_payment_id=payment_intent['id'])
# #         payment.status = 'failed'
# #         payment.save()
# #     except Payment.DoesNotExist:
# #         pass

##########################

# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# import stripe
# import json
# from .models import Payment

# stripe.api_key = settings.STRIPE_SECRET_KEY

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         return HttpResponse(status=400)

#     # Handle checkout session completed events
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         try:
#             payment = Payment.objects.get(stripe_payment_id=session['id'])
#             payment.status = 'succeeded'
#             payment.save()
#             # Optionally, add order fulfillment logic here.
#         except Payment.DoesNotExist:
#             pass

#     return HttpResponse(status=200)




# Webhook view in payments/webhooks.py

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import json
from .models import Payment
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
#         print("Webhook event received:", event)
#     except ValueError as e:
#         print("Invalid payload:", e)
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         print("Invalid signature:", e)
#         return HttpResponse(status=400)

#     # Process the event types you're interested in:
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         try:
#             payment = Payment.objects.get(stripe_payment_id=session['id'])
#             payment.status = 'succeeded'
#             payment.save()
#             print("Payment updated to succeeded for Payment ID:", payment.id)
#         except Payment.DoesNotExist:
#             print("Payment not found for session id:", session['id'])
#     # Add additional event types as needed.
    
#     return HttpResponse(status=200)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    print("Payload:", payload)
    print("Signature Header:", sig_header)
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        print("Webhook event received:", event)
    except Exception as e:
        print("Webhook error:", e)
        return HttpResponse(status=400)
    return HttpResponse(status=200)
