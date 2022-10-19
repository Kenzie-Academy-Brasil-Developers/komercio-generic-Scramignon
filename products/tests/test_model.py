from django.test import TestCase

from products.models import Product
from products.serializers import ProductSerializer

from users.models import User
from users.serializers import UserSerializer


import ipdb


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.correct_product = {
            "description":"Toothbrush",
            "price":5.99,
            "quantity":1,
        }
        cls.user_data = {
	        "username":"ale",
	        "password":"1234",
	        "first_name":"alexandre",
	        "last_name":"alves",
	        "is_seller":True
        }
        cls.product = Product.objects.create(**cls.correct_product)
        cls.user = User.objects.create_user(**cls.user_data)
    
    def test_product_creation(self):
        self.assertEqual(self.product.description, self.correct_product["description"])
        self.assertEqual(self.product.price, self.correct_product["price"])
        self.assertEqual(self.product.quantity, self.correct_product["quantity"])
        self.assertTrue(self.product.is_active)
    
    def test_product_user_relation(self):
        self.product.user = self.user
        self.product.save()

        self.assertEqual(self.product.user.id, self.user.id)

    def test_product_user_relation_serializer(self):

        # adds user (id) to product data
        self.correct_product["user"] = self.user.id
    
        serializer = ProductSerializer(data=self.correct_product)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_product = serializer.data

        self.assertEqual(new_product["id"], self.user.products.values()[0]["id"])
