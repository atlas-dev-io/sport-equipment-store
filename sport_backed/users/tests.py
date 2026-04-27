from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.repositories.user_repository import UserRepository

User = get_user_model()


class AuthControllerTests(APITestCase):
    def test_register_returns_jwt_and_profile_can_be_fetched(self):
        response = self.client.post(
            reverse("user-register"),
            {
                "username": "new-user",
                "password": "strongpass123",
                "confirm_password": "strongpass123",
                "email": "new-user@example.com",
                "nickname": "Runner",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code"], 200)
        self.assertIn("token", response.data["data"])
        self.assertIn("refresh_token", response.data["data"])

        me_client = self.client_class()
        me_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['data']['token']}")
        me_response = me_client.get(reverse("user-current"))

        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data["data"]["username"], "new-user")
        self.assertEqual(me_response.data["data"]["nickname"], "Runner")

    def test_login_returns_jwt_for_existing_user(self):
        user = UserRepository.create_user(
            username="existing-user",
            password="strongpass123",
            email="existing-user@example.com",
        )
        UserRepository.create_user_profile(user=user)

        response = self.client.post(
            reverse("user-login"),
            {
                "username": "existing-user",
                "password": "strongpass123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["code"], 200)
        self.assertEqual(response.data["data"]["user_id"], user.id)
        self.assertIn("token", response.data["data"])
        self.assertIn("refresh_token", response.data["data"])

    def test_logout_revokes_current_access_token(self):
        user = UserRepository.create_user(
            username="logout-user",
            password="strongpass123",
            email="logout-user@example.com",
        )
        UserRepository.create_user_profile(user=user)

        login_response = self.client.post(
            reverse("user-login"),
            {
                "username": "logout-user",
                "password": "strongpass123",
            },
            format="json",
        )
        access_token = login_response.data["data"]["token"]

        auth_client = self.client_class()
        auth_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        me_before_logout = auth_client.get(reverse("user-current"))
        self.assertEqual(me_before_logout.status_code, status.HTTP_200_OK)

        logout_response = auth_client.post(reverse("user-logout"))
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        me_after_logout = auth_client.get(reverse("user-current"))
        self.assertEqual(me_after_logout.status_code, status.HTTP_401_UNAUTHORIZED)
