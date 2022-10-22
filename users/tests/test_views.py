from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User

"""
Tests registration view
"""


class UserRegisterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.register_url = "/api/accounts/"
        cls.user_data_seller = {
            "username": "ale",
            "password": "1234",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": True,
        }
        cls.user_data_non_seller = {
            "username": "luci",
            "password": "1234",
            "first_name": "Lucira",
            "last_name": "Silva",
            "is_seller": False,
        }
        cls.user_data_wrong_format = {
            "username": 1,
            "password": 2,
            "first_name": False,
            "last_name": True,
            "is_seller": None,
        }

    def test_seller_creation(self):
        data = self.user_data_seller
        url = self.register_url
        response = self.client.post(url, data, format="json")
        created_user = User.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        self.assertEqual(created_user.username, data["username"])

        self.assertTrue(created_user.is_seller)
        self.assertFalse(created_user.is_superuser)

    def test_non_seller_creation(self):
        data = self.user_data_non_seller
        url = self.register_url
        response = self.client.post(url, data, format="json")
        created_user = User.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        self.assertEqual(created_user.username, data["username"])

        self.assertFalse(created_user.is_seller)
        self.assertFalse(created_user.is_superuser)

    def test_wrong_keys_creation(self):
        data = self.user_data_wrong_format
        url = self.register_url

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data["is_seller"][0], ErrorDetail)

    def test_empty_body_creation(self):
        data = {}
        url = self.register_url

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["username"][0].code, "required")
        self.assertEqual(response.data["last_name"][0].code, "required")
        self.assertEqual(response.data["first_name"][0].code, "required")
        self.assertEqual(response.data["password"][0].code, "required")


"""
Test login view
"""


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.register_url = "/api/accounts/"
        cls.login_url = "/api/login/"

        cls.user_data_seller = {
            "username": "ale",
            "password": "1234",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": True,
        }

        cls.seller_login_data = {"username": "ale", "password": "1234"}

        cls.user_data_non_seller = {
            "username": "luci",
            "password": "1234",
            "first_name": "Lucira",
            "last_name": "Silva",
            "is_seller": False,
        }

        cls.non_seller_login_data = {"username": "luci", "password": "1234"}

        cls.wrong_login_data = {"username": "leeroy", "password": "jenkins"}

    def test_seller_login(self):

        url = self.login_url
        data = self.seller_login_data

        # creates user (seller)
        self.client.post(self.register_url, self.user_data_seller, format="json")

        # makes request
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["token"])

    def test_non_seller_login(self):

        url = self.login_url
        data = self.non_seller_login_data

        # creates user (non seller)
        self.client.post(self.register_url, self.user_data_non_seller, format="json")

        # make the request
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK),
        self.assertTrue(response.data["token"])

    def test_login_wrong_data(self):

        url = self.login_url
        data = self.wrong_login_data

        # attempt to create user
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0].code, "authorization")

    def test_login_empty_data(self):

        url = self.login_url
        data = {}

        # attempt to create user
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.data["username"][0].code, "required")
        self.assertEqual(response.data["password"][0].code, "required")


"""
Test routes permission
"""


class PermissionsRoutesViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.list_url = "/api/accounts/"
        cls.register_url = "/api/accounts/"
        cls.acctivate_deactivate_url = "/api/accounts/<str:pk>/management/"
        cls.login_url = "/api/login/"
        cls.patch_url = "/api/accounts/<str:pk>/"

        cls.user_data_seller = {
            "username": "ale",
            "password": "1234",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": True,
        }

        cls.seller_login_data = {"username": "ale", "password": "1234"}

        cls.user_data_non_seller = {
            "username": "luci",
            "password": "1234",
            "first_name": "Lucira",
            "last_name": "Silva",
            "is_seller": False,
        }

        cls.non_seller_login_data = {"username": "luci", "password": "1234"}

        cls.user_data_admin = {
            "username": "fs1",
            "password": "1234",
            "first_name": "fernando",
            "last_name": "scramignon",
            "is_seller": False,
            "is_superuser": True,
        }

        cls.admin_login_data = {"username": "fs1", "password": "1234"}

    def test_anyone_can_list_users(self):

        self.client.post(self.list_url, self.user_data_seller, format="json")
        self.client.post(self.list_url, self.user_data_non_seller, format="json")

        url = self.list_url
        response = self.client.get(url, format="json")

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(
            response.data["results"][0]["username"], self.user_data_seller["username"]
        )
        self.assertEqual(
            response.data["results"][1]["username"],
            self.user_data_non_seller["username"],
        )

    def test_only_admin_can_deactivate_and_reactivate_account(self):
        self.client.post(self.register_url, self.user_data_seller, format="json")

        superuser = User.objects.create_superuser(**self.user_data_admin)
        normal_user = User.objects.get(username=self.user_data_seller["username"])

        seller_token = self.client.post(
            self.login_url, self.seller_login_data, format="json"
        ).data["token"]
        admin_token = self.client.post(
            self.login_url, self.admin_login_data, format="json"
        ).data["token"]

        url = self.acctivate_deactivate_url.replace("<str:pk>", str(normal_user.id))

        unauthorized_response = self.client.patch(
            url,
            {"is_active": False},
            format="json",
            HTTP_AUTHORIZATION=f"Token {seller_token}",
        )

        self.assertEqual(unauthorized_response.status_code, status.HTTP_403_FORBIDDEN)

        authorized_deactivation_response = self.client.patch(
            url,
            {"is_active": False},
            format="json",
            HTTP_AUTHORIZATION=f"Token {admin_token}",
        )

        self.assertEqual(
            authorized_deactivation_response.status_code, status.HTTP_200_OK
        )
        self.assertFalse(User.objects.get(username="ale").is_active)

        authorized_activation_response = self.client.patch(
            url,
            {"is_active": True},
            format="json",
            HTTP_AUTHORIZATION=f"Token {admin_token}",
        )

        self.assertEqual(authorized_activation_response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.get(username="ale").is_active)

    def test_only_owner_can_patch_account(self):
        # creates users
        self.client.post(self.register_url, self.user_data_seller, format="json")
        self.client.post(self.register_url, self.user_data_non_seller, format="json")

        # makes login with both users
        seller_token = self.client.post(
            self.login_url, self.seller_login_data, format="json"
        ).data["token"]
        non_seller_token = self.client.post(
            self.login_url, self.non_seller_login_data, format="json"
        ).data["token"]

        # get users
        seller_user = User.objects.get(username="ale")
        non_seller_user = User.objects.get(username="luci")

        # set up patch data
        url = self.patch_url.replace("<str:pk>", str(non_seller_user.id))
        data = {"last_name": "patched"}

        # tries to patch user without being him
        non_owner_response = self.client.patch(
            url, data, format="json", HTTP_AUTHORIZATION=f"Token {seller_token}"
        )

        self.assertEqual(non_owner_response.status_code, status.HTTP_403_FORBIDDEN)

        # tries to patch user while being him
        owner_response = self.client.patch(
            url, data, format="json", HTTP_AUTHORIZATION=f"Token {non_seller_token}"
        )

        self.assertEqual(owner_response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(username="luci").last_name, data["last_name"])
