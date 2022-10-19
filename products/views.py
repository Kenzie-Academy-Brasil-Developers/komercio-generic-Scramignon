from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .permissions import IsSellerOrReadOnly, IsSellerOwnerOrReadOnly

from .models import Product

from .serializers import PostProductSerializer, ProductSerializer


# Create your views here.
class ProductsView(generics.ListCreateAPIView):

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        return self.create(request, *args, **kwargs)

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    serializer_map = {
        'GET': ProductSerializer,
        'POST': PostProductSerializer,
    }

    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOwnerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = PostProductSerializer