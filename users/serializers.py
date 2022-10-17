from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser"
        ]

        read_only_fields = [
            "date_joined",
            "is_active",
            "is_superuser"
        ]

        extra_kwargs = {
            "username": {"validators":[UniqueValidator(queryset=User.objects.all())]},
            "password": {"write_only":True}
        }

