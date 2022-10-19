from django.test import TestCase
from users.models import User
from products.models import Product

import ipdb

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
	        "username":"ale",
	        "password":"1234",
	        "first_name":"alexandre",
	        "last_name":"alves",
	        "is_seller":True
        }

        cls.user = User.objects.create_user(**cls.user_data)

        cls.correct_product = {
            "description":"Toothbrush",
            "price":5.99,
            "quantity":1,
            "user":cls.user
        }

        cls.product = Product.objects.create(**cls.correct_product)
        cls.product_2 = Product.objects.create(**cls.correct_product)

    def test_user_creation(self):
        self.assertEqual(self.user.username, self.user_data["username"])
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertEqual(self.user.is_seller, self.user_data["is_seller"])
    
    def test_user_products_relation(self):
        # user can have multiple products
        self.assertEqual(self.product.id, self.user.products.values()[0]["id"])
        self.assertEqual(self.product_2.id, self.user.products.values()[1]["id"])