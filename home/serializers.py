from .models import *
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"