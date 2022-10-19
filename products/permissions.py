from rest_framework.permissions import BasePermission

import ipdb

# when changing app name from user to accounts don't forget to modify this

class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        
        return (
            request.user.is_authenticated
            and request.user.is_seller
        )

class IsSellerOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        
        return (
            request.user.is_authenticated
            and request.user.is_seller
            and request.user.id == obj.user_id
        )