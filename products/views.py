from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .permissions import IsSellerOrReadOnly, IsSellerOwnerOrReadOnly

from .models import Product

from .serializers import PostProductSerializer, ProductSerializer


# Create your views here.
class ProductsView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    # allow custom serializers for different methods
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)

    serializer_map = {
        'GET': ProductSerializer,
        'POST': PostProductSerializer,
    }

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)



    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOwnerOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)

    serializer_map = {
        'GET': ProductSerializer,
        'Patch': PostProductSerializer,
    }

    queryset = Product.objects
    serializer_class = PostProductSerializer