from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories']
        read_only_fields = ['id']

    def get_subcategories(self, obj):
        # Recursively serialize all subcategories
        subcats = obj.subcategories.all()
        return CategorySerializer(subcats, many=True).data if subcats.exists() else []

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']  # Admins/sellers cannot modify these fields

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = ['id','product','rating','comment']
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
