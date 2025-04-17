# from rest_framework import serializers
# from .models import Order, OrderItem

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'price']
#         read_only_fields = ['price']

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True,required=False)

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'items', 'status', 'total', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'total', 'created_at', 'updated_at']

# from rest_framework import serializers
# from .models import Order, OrderItem

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'price']
#         read_only_fields = ['price']

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, required=False)
#     total = serializers.SerializerMethodField()  # computed total

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'items', 'status', 'total', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'created_at', 'updated_at']

#     def get_total(self, obj):
#         # Calculate the total dynamically from the order items.
#         return sum(item.price * item.quantity for item in obj.items.all())



# from rest_framework import serializers
# from .models import Order, OrderItem

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'price']
#         read_only_fields = ['price']

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, required=False)
#     total = serializers.SerializerMethodField()  # Computed total

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'items', 'status', 'total', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'created_at', 'updated_at']

#     def get_total(self, obj):
#         # Calculate the total dynamically from the order items.
#         return sum(item.price * item.quantity for item in obj.items.all())




# import json
# from rest_framework import serializers
# from .models import Order, OrderItem

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'price']
#         read_only_fields = ['price']

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, required=False)
#     total = serializers.SerializerMethodField()  # Computed total

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'items', 'status', 'total', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'created_at', 'updated_at', 'total']

#     def get_total(self, obj):
#         # Calculate the total dynamically from the order items.
#         return sum(item.price * item.quantity for item in obj.items.all())

#     def create(self, validated_data):
#         # Try to get nested items data, if provided.
#         items_data = validated_data.pop('items', None)
        
#         # If no nested 'items' is provided, check for individual keys.
#         if items_data is None:
#             product = self.initial_data.get('product')
#             quantity = self.initial_data.get('quantity')
#             if product and quantity:
#                 try:
#                     # Convert to integers if necessary.
#                     product = int(product)
#                     quantity = int(quantity)
#                 except ValueError:
#                     raise serializers.ValidationError("Product and quantity must be valid integers.")
#                 items_data = [{"product": product, "quantity": quantity}]
#             else:
#                 items_data = []
#         else:
#             # If items_data is a string (as is common with form-data), try to parse it.
#             if isinstance(items_data, str):
#                 try:
#                     items_data = json.loads(items_data)
#                 except json.JSONDecodeError:
#                     raise serializers.ValidationError("Invalid JSON format for items.")
        
#         # Create the order instance.
#         order = Order.objects.create(**validated_data)
        
#         # Create each OrderItem using the provided data.
#         for item in items_data:
#             OrderItem.objects.create(order=order, **item)
#         return order



# import json
# from rest_framework import serializers
# from .models import Order, OrderItem

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'price']
#         read_only_fields = ['price']

# class OrderSerializer(serializers.ModelSerializer):
#     # This field supports nested input but if DRF parses it as an empty list,
#     # we’ll check the raw input.
#     items = OrderItemSerializer(many=True, required=False)
#     total = serializers.SerializerMethodField()  # Computed total

#     # These fields allow individual product/quantity input.
#     product = serializers.IntegerField(write_only=True, required=False)
#     quantity = serializers.IntegerField(write_only=True, required=False)

#     class Meta:
#         model = Order
#         fields = [
#             'id', 'user', 'items', 'status', 'total',
#             'created_at', 'updated_at', 'product', 'quantity'
#         ]
#         read_only_fields = ['user', 'created_at', 'updated_at', 'total']

#     def get_total(self, obj):
#         return sum(item.price * item.quantity for item in obj.items.all())

#     def create(self, validated_data):
#         # First, try to pop out any nested "items" from validated_data.
#         items_data = validated_data.pop('items', None)
#         # If DRF parsed "items" as an empty list, check raw input.
#         if (items_data is None or items_data == []) and 'items' in self.initial_data:
#             items_raw = self.initial_data.get('items')
#             if isinstance(items_raw, str):
#                 try:
#                     items_data = json.loads(items_raw)
#                 except json.JSONDecodeError:
#                     raise serializers.ValidationError("Invalid JSON format for items.")
#         # If still no items data, try to get individual product and quantity fields.
#         if not items_data:
#             product = validated_data.pop('product', None) or self.initial_data.get('product')
#             quantity = validated_data.pop('quantity', None) or self.initial_data.get('quantity')
#             if product and quantity:
#                 try:
#                     product = int(product)
#                     quantity = int(quantity)
#                 except ValueError:
#                     raise serializers.ValidationError("Product and quantity must be valid integers.")
#                 items_data = [{"product": product, "quantity": quantity}]
#             else:
#                 items_data = []
#         # Create the Order instance.
#         order = Order.objects.create(**validated_data)
#         # Create each OrderItem associated with the order.
#         for item in items_data:
#             OrderItem.objects.create(order=order, **item)
#         return order


# from rest_framework import serializers
# from .models import Order, OrderItem

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'price']
#         read_only_fields = ['price']

# class OrderSerializer(serializers.ModelSerializer):
#     # The items field is now read-only and will be populated after order item creation.
#     items = OrderItemSerializer(many=True, read_only=True)
#     total = serializers.SerializerMethodField(read_only=True)
    
#     # These are the only writable fields from the client.
#     product = serializers.IntegerField(write_only=True, required=True)
#     quantity = serializers.IntegerField(write_only=True, required=True)

#     class Meta:
#         model = Order
#         fields = [
#             'id', 'user', 'items', 'status', 'total',
#             'created_at', 'updated_at', 'product', 'quantity'
#         ]
#         read_only_fields = ['user', 'items', 'total', 'created_at', 'updated_at']

#     def get_total(self, obj):
#         return sum(item.price * item.quantity for item in obj.items.all())

#     def create(self, validated_data):
#         # Extract the individual product and quantity.
#         product = validated_data.pop('product')
#         quantity = validated_data.pop('quantity')
#         # Create the Order instance.
#         order = Order.objects.create(**validated_data)
#         # Create the OrderItem using the provided product and quantity.
#         OrderItem.objects.create(order=order, product=product, quantity=quantity)
#         return order

# from rest_framework import serializers
# from .models import Order, OrderItem
# from catalog.models import Product  # Adjust the import based on your project structure

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'price']
#         read_only_fields = ['price']

# class OrderSerializer(serializers.ModelSerializer):
#     # The items field is now read-only and will be populated after order item creation.
#     items = OrderItemSerializer(many=True, read_only=True)
#     total = serializers.SerializerMethodField(read_only=True)
    
#     # Only these fields are writable via form-data.
#     product = serializers.IntegerField(write_only=True, required=True)
#     quantity = serializers.IntegerField(write_only=True, required=True)

#     class Meta:
#         model = Order
#         fields = [
#             'id', 'user', 'items', 'status', 'total',
#             'created_at', 'updated_at', 'product', 'quantity'
#         ]
#         read_only_fields = ['user', 'items', 'total', 'created_at', 'updated_at']

#     def get_total(self, obj):
#         return sum(item.price * item.quantity for item in obj.items.all())

#     def create(self, validated_data):
#         # Extract product ID and quantity from validated data.
#         product_id = validated_data.pop('product')
#         quantity = validated_data.pop('quantity')
#         # Create the Order instance.
#         order = Order.objects.create(**validated_data)
        
#         # Look up the Product instance by ID.
#         try:
#             product_instance = Product.objects.get(pk=product_id)
#         except Product.DoesNotExist:
#             raise serializers.ValidationError({"product": "Invalid product id."})
        
#         # Create the OrderItem with the actual Product instance.
#         OrderItem.objects.create(order=order, product=product_instance, quantity=quantity,price=product_instance.price )
#         return order


from rest_framework import serializers
from .models import Order, OrderItem
from catalog.models import Product  # Adjust the import based on your project structure

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        read_only_fields = ['price']

class OrderSerializer(serializers.ModelSerializer):
    # The items field is now read-only and will be populated after order item creation.
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    
    # Only these fields are writable via form-data.
    product = serializers.IntegerField(write_only=True, required=True)
    quantity = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'items', 'status', 'total',
            'created_at', 'updated_at', 'product', 'quantity'
        ]
        read_only_fields = ['user', 'items', 'total', 'created_at', 'updated_at']

    def get_total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())

    def create(self, validated_data):
        # Extract product ID and quantity from validated data.
        product_id = validated_data.pop('product')
        quantity = validated_data.pop('quantity')
        # Create the Order instance.
        order = Order.objects.create(**validated_data)
        
        # Look up the Product instance by ID.
        try:
            product_instance = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product": "Invalid product id."})
        
        # Create the OrderItem with the actual Product instance.
        OrderItem.objects.create(
            order=order,
            product=product_instance,
            quantity=quantity,
            price=product_instance.price  # Set price from product
        )
        return order

    def update(self, instance, validated_data):
        # Extract product ID and quantity if provided in update.
        product_id = validated_data.pop('product', None)
        quantity = validated_data.pop('quantity', None)
        
        # Update fields on the Order instance (for example, status).
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        
        # If both product and quantity are provided, update or create the OrderItem.
        if product_id is not None and quantity is not None:
            try:
                product_instance = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product": "Invalid product id."})
            
            # Update the first OrderItem if it exists; otherwise, create a new one.
            order_item = instance.items.first()
            if order_item:
                order_item.product = product_instance
                order_item.quantity = quantity
                order_item.price = product_instance.price
                order_item.save()
            else:
                OrderItem.objects.create(
                    order=instance,
                    product=product_instance,
                    quantity=quantity,
                    price=product_instance.price
                )
        return instance
