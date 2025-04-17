

# ##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# from rest_framework import viewsets, status, views
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django_filters.rest_framework import DjangoFilterBackend
# import stripe
# from django.conf import settings
# from django.shortcuts import redirect
# from .models import Payment
# from .serializers import PaymentSerializer, PaymentIntentSerializer

# # Set your Stripe API key
# stripe.api_key = settings.STRIPE_SECRET_KEY

# class PaymentViewSet(viewsets.ModelViewSet):
#     """
#     Handles listing and creating Payment records and provides a custom action to download a receipt.
#     """
#     serializer_class = PaymentSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]

#     def get_queryset(self):
#         return Payment.objects.filter(user=self.request.user)
    
#     def create(self, request, *args, **kwargs):
#         """
#         Creates a Stripe Checkout Session and a Payment record.
#         Expects an order_id (and optionally currency) from the client.
#         """
#         intent_serializer = PaymentIntentSerializer(data=request.data)
#         intent_serializer.is_valid(raise_exception=True)
        
#         order_id = intent_serializer.validated_data['order_id']
#         currency = intent_serializer.validated_data.get('currency') or 'inr'
        
#         # Import Order model (assuming it's in orders.models)
#         from orders.models import Order
#         try:
#             order = Order.objects.get(id=order_id)
#         except Order.DoesNotExist:
#             return Response({"error": "Invalid order id."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Build line items from order's items (assumes order.items exists)
#         line_items = []
#         if not order.items.exists():
#             return Response({"error": "Order has no items."}, status=status.HTTP_400_BAD_REQUEST)
        
#         for item in order.items.all():
#             product = item.product
#             line_items.append({
#                 'price_data': {
#                     'currency': currency,
#                     'unit_amount': int(product.price * 100),  # convert to smallest currency unit
#                     'product_data': {
#                         'name': product.name,
#                         'description': getattr(product, 'description', ''),
#                         'images': [product.image.url] if hasattr(product, 'image') and product.image else [],
#                     },
#                 },
#                 'quantity': item.quantity,
#             })
        
#         try:
#             # Create a Stripe Checkout Session with invoice creation enabled
#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 invoice_creation={"enabled": True},
#                 billing_address_collection='required',
#                 success_url=settings.DOMAIN + 'success/',
#                 cancel_url=settings.DOMAIN + 'cancel/',
#                 customer_email=request.user.email,
#                 metadata={'order_id': order.id}
#             )
#             # Create a Payment record
#             payment = Payment.objects.create(
#                 user=request.user,
#                 order=order,
#                 amount=order.total,  # Assumes order.total is defined (in rupees)
#                 stripe_payment_id=checkout_session.id,
#                 status='pending'
#             )
#             payment_data = PaymentSerializer(payment).data
#             payment_data['checkout_session_url'] = checkout_session.url
#             return Response(payment_data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=True, methods=['get'], url_path='receipt', permission_classes=[IsAuthenticated])
#     def receipt(self, request, pk=None):
#         """
#         Custom action to download the receipt for a payment.
#         Accessible via: GET /payment/<pk>/receipt/
#         """
#         try:
#             payment = self.get_queryset().get(pk=pk)
#         except Payment.DoesNotExist:
#             return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

#         if payment.status != 'succeeded':
#             return Response({"error": "Payment not completed yet."}, status=status.HTTP_400_BAD_REQUEST)

#         if not payment.hosted_invoice_url:
#             return Response({"error": "Receipt not available."}, status=status.HTTP_404_NOT_FOUND)

#         # Redirect to the Stripe-hosted invoice URL for receipt download.
#         return redirect(payment.hosted_invoice_url)


# class StripeWebhookView(views.APIView):
#     """
#     Handles incoming Stripe webhook events.
#     Also generates an invoice after a successful checkout session.
#     """
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         payload = request.body
#         sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#             )
#             print("Webhook event received:", event)
#         except ValueError as e:
#             print("Invalid payload:", e)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         except stripe.error.SignatureVerificationError as e:
#             print("Invalid signature:", e)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#         # Process checkout session completion event
#         if event['type'] == 'checkout.session.completed':
#             session = event['data']['object']
#             order_id = session.get("metadata", {}).get("order_id")
#             try:
#                 payment = Payment.objects.get(id=order_id)
#                 payment.status = 'succeeded'
#                 payment.save()
#                 print("Payment updated to succeeded for Payment ID:", payment.id)
#             except Payment.DoesNotExist:
#                 print("Payment not found for session id:", session.get('id'))
            
#             # Invoice generation
#             customer_id = session.get("customer")
#             try:
#                 # Create an invoice item for the payment amount (convert to paise if INR)
#                 stripe.InvoiceItem.create(
#                     customer=customer_id,
#                     amount=int(payment.amount * 100),
#                     currency="inr",
#                     description=f"Invoice for Order #{order_id}"
#                 )
#                 # Create and auto-finalize the invoice
#                 invoice = stripe.Invoice.create(
#                     customer=customer_id,
#                     auto_advance=True
#                 )
#                 invoice_pdf_url = invoice.invoice_pdf
#                 print("Invoice created with ID:", invoice.id)
#                 print("Invoice PDF URL:", invoice_pdf_url)
#                 # Update the Payment record with the hosted invoice URL
#                 payment.hosted_invoice_url = invoice_pdf_url
#                 payment.save()
#             except Exception as e:
#                 print("Invoice creation error:", e)
        
#         # Process additional event types as needed.

#         return Response(status=status.HTTP_200_OK)


############################################################################################################################################
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
import stripe
from django.conf import settings
from django.shortcuts import redirect
from .models import Payment
from .serializers import PaymentSerializer, PaymentIntentSerializer

# Set your Stripe API key from settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentViewSet(viewsets.ModelViewSet):
    """
    Handles listing and creating Payment records and provides custom actions
    to download a receipt and process refunds.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Creates a Stripe Checkout Session and a Payment record.
        Expects an order_id (and optionally currency) from the client.
        """
        intent_serializer = PaymentIntentSerializer(data=request.data)
        intent_serializer.is_valid(raise_exception=True)
        
        order_id = intent_serializer.validated_data['order_id']
        currency = intent_serializer.validated_data.get('currency') or 'inr'
        
        # Import Order model (assuming it's in orders.models)
        from orders.models import Order
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Invalid order id."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Build line items from order's items (assumes order.items exists)
        line_items = []
        if not order.items.exists():
            return Response({"error": "Order has no items."}, status=status.HTTP_400_BAD_REQUEST)
        
        for item in order.items.all():
            product = item.product
            line_items.append({
                'price_data': {
                    'currency': currency,
                    'unit_amount': int(product.price * 100),  # convert to smallest currency unit
                    'product_data': {
                        'name': product.name,
                        'description': getattr(product, 'description', ''),
                        'images': [product.image.url] if hasattr(product, 'image') and product.image else [],
                    },
                },
                'quantity': item.quantity,
            })
        
        try:
            # Create a Stripe Checkout Session with invoice creation enabled
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                invoice_creation={"enabled": True},
                billing_address_collection='required',
                success_url=settings.DOMAIN + 'success/',
                cancel_url=settings.DOMAIN + 'cancel/',
                customer_email=request.user.email,
                metadata={'order_id': order.id}
            )
            # Create a Payment record
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total,  # Assumes order.total is defined (in rupees)
                stripe_payment_id=checkout_session.id,
                status='pending'
            )
            payment_data = PaymentSerializer(payment).data
            payment_data['checkout_session_url'] = checkout_session.url
            return Response(payment_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='receipt', permission_classes=[IsAuthenticated])
    def receipt(self, request, pk=None):
        """
        Custom action to download the receipt for a payment.
        Accessible via: GET /payment/<pk>/receipt/
        """
        try:
            payment = self.get_queryset().get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        if payment.status != 'succeeded':
            return Response({"error": "Payment not completed yet."}, status=status.HTTP_400_BAD_REQUEST)

        if not payment.hosted_invoice_url:
            return Response({"error": "Receipt not available."}, status=status.HTTP_404_NOT_FOUND)

        # Redirect to the Stripe-hosted invoice URL for receipt download.
        return redirect(payment.hosted_invoice_url)
    
    @action(detail=True, methods=['post'], url_path='refund', permission_classes=[IsAuthenticated])
    def refund(self, request, pk=None):
        """
        Custom action to process a refund for a payment.
        Accepts an optional 'amount' in rupees for a partial refund.
        Accessible via: POST /payment/<pk>/refund/
        """
        try:
            payment = self.get_queryset().get(pk=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if payment.status != 'succeeded':
            return Response({"error": "Only succeeded payments can be refunded."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Optional 'amount' for partial refund (expected in rupees)
        refund_amount = request.data.get('amount')
        
        try:
            if refund_amount:
                # Convert to smallest currency unit (e.g., paise for INR)
                refund_amount_int = int(float(refund_amount) * 100)
                refund = stripe.Refund.create(
                    charge=payment.stripe_payment_id,
                    amount=refund_amount_int
                )
                # Update status to indicate partial refund (custom; adjust as needed)
                payment.status = 'partial_refunded'
            else:
                refund = stripe.Refund.create(
                    charge=payment.stripe_payment_id
                )
                payment.status = 'refunded'
            payment.save()
            return Response({"message": "Refund processed successfully.", "refund": refund}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StripeWebhookView(views.APIView):
    """
    Handles incoming Stripe webhook events.
    Also generates an invoice after a successful checkout session.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
            print("Webhook event received:", event)
        except ValueError as e:
            print("Invalid payload:", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            print("Invalid signature:", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # Process checkout session completion event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order_id = session.get("metadata", {}).get("order_id")
            try:
                payment = Payment.objects.get(id=order_id)
                payment.status = 'succeeded'
                payment.save()
                print("Payment updated to succeeded for Payment ID:", payment.id)
            except Payment.DoesNotExist:
                print("Payment not found for session id:", session.get('id'))
            
            # Invoice generation
            customer_id = session.get("customer")
            try:
                # Create an invoice item for the payment amount (convert to paise if INR)
                stripe.InvoiceItem.create(
                    customer=customer_id,
                    amount=int(payment.amount * 100),
                    currency="inr",
                    description=f"Invoice for Order #{order_id}"
                )
                # Create and auto-finalize the invoice
                invoice = stripe.Invoice.create(
                    customer=customer_id,
                    auto_advance=True
                )
                invoice_pdf_url = invoice.invoice_pdf
                print("Invoice created with ID:", invoice.id)
                print("Invoice PDF URL:", invoice_pdf_url)
                # Update the Payment record with the hosted invoice URL
                payment.hosted_invoice_url = invoice_pdf_url
                payment.save()
            except Exception as e:
                print("Invoice creation error:", e)
        
        # Process additional event types as needed.

        return Response(status=status.HTTP_200_OK)
