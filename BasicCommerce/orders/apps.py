    # orders/apps.py

from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'  # Ensure this matches your app folder name

    def ready(self):
        # Import the signals module so that your signal handlers are registered.
        import orders.signals
