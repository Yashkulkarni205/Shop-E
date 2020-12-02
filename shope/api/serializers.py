from rest_framework import serializers
import sys
sys.path.append("..")
from shop.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
