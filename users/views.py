from rest_framework import views
from rest_framework import generics

from rest_framework.authentication import TokenAuthentication


from .models import User
from .serializers import UserSerializer


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class listNewUsersView(generics.ListAPIView):

    def get_queryset(self):
        num = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[:num]
    
    queryset = User.objects.all()
    serializer_class = UserSerializer