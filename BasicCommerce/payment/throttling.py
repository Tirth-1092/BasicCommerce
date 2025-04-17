from rest_framework.throttling import UserRateThrottle

class PaymentThrottle(UserRateThrottle):
    scope = 'payment'
