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
            "password": {"write_only":True},
            "is_active":{"read_only":True}
        }
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)

        try:
            user.set_password(validated_data["password"])
            user.save()
        except KeyError:
            pass
    
        return user

class UserActiveToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser"
        ]

        read_only_fields = [
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser"
        ]

