from wsgiref import validate
from django.test import TestCase

from products.models import Product
from products.serializers import ProductSerializer

from users.models import User
from users.serializers import UserSerializer


import ipdb

from utils.validators import validate_2_decimal_places


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
	        "username":"ale",
	        "password":"1234",
	        "first_name":"alexandre",
	        "last_name":"alves",
	        "is_seller":True
        }

        cls.user_data_2 = {
            "username":"ale2",
	        "password":"1234",
	        "first_name":"alexandre",
	        "last_name":"alves",
	        "is_seller":True
        }

        cls.user = User.objects.create_user(**cls.user_data)
        cls.user_2 = User.objects.create_user(**cls.user_data_2)

        cls.correct_product = {
            "description":"Toothbrush",
            "price":5.99,
            "quantity":1,
            "user":cls.user
        }

        cls.product = Product.objects.create(**cls.correct_product)
    
    def test_product_creation(self):
        self.assertEqual(self.product.description, self.correct_product["description"])
        self.assertEqual(self.product.price, self.correct_product["price"])
        self.assertEqual(self.product.quantity, self.correct_product["quantity"])
        self.assertTrue(self.product.is_active)

    
    def test_product_user_relation(self):
        # product can have one user
        self.assertEqual(self.product.user.id, self.user.id)

        self.product.user = self.user_2
        self.product.save()

        # but one user only
        self.assertEqual(self.product.user.id, self.user_2.id)
        self.assertFalse(self.user.products.values())

    # def test_product_user_relation_serializer(self):

    #     # adds user (id) to product data
    #     self.correct_product["user"] = self.user.id
    
    #     serializer = ProductSerializer(data=self.correct_product)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     new_product = serializer.data

    #     self.assertEqual(self.product.id, self.user.products.values()[0]["id"])
    #     self.assertEqual(new_product["id"], str(self.user.products.values()[1]["id"]))

