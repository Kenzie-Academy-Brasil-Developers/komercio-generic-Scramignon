from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from ..models import Product

class TestProductRegisterView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product_data = {
            "description":"soap",
            "price":2.99,
            "quantity":1
        }

        cls.wrong_product_data = {
            "description":False,
            "price":True,
            "quantity":"i am sad"
        }

        cls.negative_quantity_product_data = {
            "description":"sopa",
            "price":1.99,
            "quantity":-2
        }
        
        cls.seller_user_data = {
            "username":"ale",
            "password":"1234",
            "first_name":"alexandre",
            "last_name":"alves",
            "is_seller":True
        }

        cls.seller_login_data = {
            "username":"ale",
            "password":"1234"
        }

        cls.non_seller_user_data = {
            "username":"luci",
            "password":"1234",
            "first_name":"lucira",
            "last_name":"silva",
            "is_seller":False
        }

        cls.non_seller_login_data = {
            "username":"luci",
            "password":"1234"
        }

        cls.register_user_url = "/api/accounts/"
        cls.login_url = "/api/login/"

        cls.register_products_url = "/api/products/"
        

    def test_seller_can_register_products(self):
        # creates seller user
        self.client.post(self.register_user_url, data=self.seller_user_data)

        # Performs login and gets its token
        seller_token = self.client.post(
            self.login_url,
            self.seller_login_data,
            format="json"
        ).data["token"]

        # set up product registration data
        url = self.register_products_url
        data = self.product_data

        # creates product
        product_creation_response = self.client.post(
            url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {seller_token}"
        )

        self.assertEqual(product_creation_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().description, data["description"])
    

    def test_non_seller_can_not_create_product(self):
        # creates non seller user
        self.client.post(self.register_user_url, self.non_seller_user_data, format="json")

        # performs login and stores token
        non_seller_token = self.client.post(
            self.login_url,
            self.non_seller_login_data,
            format="json"
        ).data["token"]

        # sets up creation data
        url = self.register_products_url
        data = self.product_data

        # creates the product
        product_creation_response = self.client.post(
            url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {non_seller_token}"
        )

        self.assertEqual(
            product_creation_response.status_code,
            status.HTTP_403_FORBIDDEN
        )
    
    def test_wrong_format_product_creation(self):
        # creates user
        self.client.post(self.register_user_url, self.seller_user_data, format="json")

        # performs login
        seller_token = self.client.post(
            self.login_url,
            self.seller_login_data,
            format="json"
        ).data["token"]

        # sets up product registration data
        url = self.register_products_url
        data = self.wrong_product_data

        # creates product
        product_creation_response = self.client.post(
            url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {seller_token}"
        )

        self.assertEqual(
            product_creation_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_creation_product_without_token(self):
        # sets up product creation data
        url = self.register_products_url
        data = self.product_data
        
        # creates product
        product_creation_response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            product_creation_response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_creating_product_with_negative_quantity(self):
        # creates user
        self.client.post(
            self.register_user_url,
            self.seller_user_data,
            format="json"
        )
        
        # login
        seller_token = self.client.post(
            self.login_url,
            self.seller_login_data,
            format="json"
        ).data["token"]

        # sets up creation data
        url = self.register_products_url
        data = self.negative_quantity_product_data

        # attempt product creation
        product_creation_response = self.client.post(
            url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {seller_token}"
        )

        self.assertEqual(
            product_creation_response.data["quantity"][0].code,
            "min_value"
        )




class TestProductUpdateView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product_data = {
            "description":"soap",
            "price":2.99,
            "quantity":1
        }

        cls.wrong_product_data = {
            "description":False,
            "price":True,
            "quantity":"i am sad"
        }

        cls.negative_quantity_product_data = {
            "description":"sopa",
            "price":1.99,
            "quantity":-2
        }
        
        cls.seller_user_data = {
            "username":"ale",
            "password":"1234",
            "first_name":"alexandre",
            "last_name":"alves",
            "is_seller":True
        }

        cls.seller_user_data_2 = {
            "username":"ale2",
            "password":"1234",
            "first_name":"alexandre2",
            "last_name":"alves2",
            "is_seller":True
        }

        cls.seller_login_data = {
            "username":"ale",
            "password":"1234"
        }

        cls.seller_login_data_2 = {
            "username":"ale2",
            "password":"1234"
        }

        cls.non_seller_user_data = {
            "username":"luci",
            "password":"1234",
            "first_name":"lucira",
            "last_name":"silva",
            "is_seller":False
        }

        cls.non_seller_login_data = {
            "username":"luci",
            "password":"1234"
        }

        cls.patch_data = {
            "quantity": 2
        }

        cls.register_user_url = "/api/accounts/"
        cls.login_url = "/api/login/"

        cls.patch_url = "/api/products/<str:pk>/"

        cls.seller = User.objects.create_user(**cls.seller_user_data)
        cls.seller_2 = User.objects.create_user(**cls.seller_user_data_2)
        
        cls.non_seller = User.objects.create_user(**cls.non_seller_user_data)

        cls.product = Product.objects.create(**cls.product_data, user=cls.seller)
    
    def test_owner_can_patch(self):

        seller_token = self.client.post(
            self.login_url,
            self.seller_login_data,
            format="json"
        ).data["token"]

        url = self.patch_url.replace("<str:pk>", str(self.product.id))
        data = self.patch_data

        patch_response = self.client.patch(
            url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {seller_token}"
        )


        self.assertEqual(
            patch_response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Product.objects.get(description="soap").quantity,
            self.patch_data["quantity"]
        )
    
    def test_non_owner_can_not_patch(self):
        # login
        seller_token_2 = self.client.post(
            self.login_url,
            self.seller_login_data_2,
            format="json"
        ).data["token"]

        # sets up patch data
        url = self.patch_url.replace("<str:pk>", str(self.product.id))
        data = self.patch_data

        patch_response = self.client.patch(
            url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {seller_token_2}"
        )

        self.assertEqual(
            patch_response.status_code,
            status.HTTP_403_FORBIDDEN
        )

class TestProductListView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.product_data = {
            "description":"soap",
            "price":2.99,
            "quantity":1
        }

        cls.product_data_2 = {
            "description":"paper",
            "price":0.99,
            "quantity":50
        }

        cls.seller_user_data = {
            "username":"ale",
            "password":"1234",
            "first_name":"alexandre",
            "last_name":"alves",
            "is_seller":True
        }

        cls.list_url = "/api/products/"
        cls.list_specific_url = "/api/products/<str:pk>/"

        cls.user = User.objects.create(**cls.seller_user_data)
        cls.product_1 = Product.objects.create(**cls.product_data, user=cls.user)
        cls.product_2 = Product.objects.create(**cls.product_data_2, user=cls.user)

    def test_anyone_can_list_products(self):
        url = self.list_url
        list_response = self.client.get(url, format="json")

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 2)
    
    def test_anyone_can_filter_products(self):
        url = self.list_specific_url.replace("<str:pk>", str(self.product_1.id))
        list_response = self.client.get(url, format="json")

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            list_response.data["description"],
            self.product_1.description
        )
    
    def test_filter_with_wrong_id(self):
        wrong_id = "60a12170-2de2-4132-84d9-d926fc87bf93"
        url = self.list_specific_url.replace("<str:pk>", wrong_id)
        list_response = self.client.get(url, format="json")
        

        self.assertEqual(list_response.status_code, status.HTTP_404_NOT_FOUND)
