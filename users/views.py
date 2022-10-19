from rest_framework import views
from rest_framework import generics

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser


from .models import User
from .serializers import UserSerializer, UserActiveToggleSerializer

from .permissions import UpdateUserPermission

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class listNewUsersView(generics.ListAPIView):

    def get_queryset(self):
        num = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[:num]
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UpdateUsersView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UpdateUserPermission]


    queryset = User.objects

    # is_active is read only. So it can't be updated 
    serializer_class = UserSerializer

class ActivationAndDeactivationView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects
    serializer_class = UserActiveToggleSerializer