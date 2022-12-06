import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from shop.models import Product



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("title", "description", "category", "price")