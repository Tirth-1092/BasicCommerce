from rest_framework.throttling import UserRateThrottle,ScopedRateThrottle

class ProductListThrottle(ScopedRateThrottle):
    scope = 'product_list'  # Define a custom scope for throttling

# class CategoryUserThrottle(UserRateThrottle):
#     rate = '10/min'  # Limit to 10 requests per minute per user
class CategoryThrottle(UserRateThrottle):
    rate = '10/min'  # Limit to 10 requests per minute per user