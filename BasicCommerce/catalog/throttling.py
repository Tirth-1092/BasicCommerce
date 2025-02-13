from rest_framework.throttling import UserRateThrottle

class ProductListThrottle(UserRateThrottle):
    scope = 'product_list'  # Define a custom scope for throttling