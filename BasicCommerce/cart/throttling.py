from rest_framework.throttling import UserRateThrottle

class CartThrottle(UserRateThrottle):
    scope = 'cart'
