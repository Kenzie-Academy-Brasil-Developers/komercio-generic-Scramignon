from rest_framework import serializers
from .models import Product
from utils.validators import validate_2_decimal_places
from users.serializers import UserSerializer

import ipdb

class PostProductSerializer(serializers.ModelSerializer):
    seller = serializers.SerializerMethodField()
    class Meta:

        model = Product
        fields = "__all__"
        read_only_fields = ["id"]

        # depth = 1
        extra_kwargs = {
            "price":{
                "validators":[validate_2_decimal_places]
            },
            "user": {
                "allow_null":True,
                "write_only":True
            }
        }

    def get_seller(self, obj):
        try:
            return UserSerializer(obj.user).data
        except AttributeError:
            return None

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product



class ProductSerializer(serializers.ModelSerializer):
    seller_id = serializers.SerializerMethodField()
    class Meta:

        model = Product
        fields = "__all__"
        read_only_fields = ["id"]

        # depth = 1
        extra_kwargs = {
            "price":{
                "validators":[validate_2_decimal_places]
            },
            "user": {
                "allow_null":True,
                "write_only":True
            }
        }

    def get_seller_id(self, obj):
        try:
            return obj.user.id
        except AttributeError:
            return None

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

