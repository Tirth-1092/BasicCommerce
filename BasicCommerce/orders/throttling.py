from rest_framework.throttling import UserRateThrottle

class OrderThrottle(UserRateThrottle):
    scope = 'order'
