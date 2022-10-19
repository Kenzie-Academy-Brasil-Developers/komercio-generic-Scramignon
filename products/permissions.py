from rest_framework.permissions import BasePermission, SAFE_METHODS

import ipdb

class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        
        return (
            request.user.is_authenticated
            and request.user.is_seller
        )