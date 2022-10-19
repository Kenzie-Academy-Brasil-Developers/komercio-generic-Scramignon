from rest_framework.views import Response
from rest_framework.permissions import BasePermission

class UpdateUserPermission(BasePermission):
    # is_active is read only. So the user won't be able to update it
    def has_object_permission(self, request, view, obj):
        if not request.user.id == obj.id:
            return False
        
        return True
        