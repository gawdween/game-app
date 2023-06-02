from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Game, PlaySession
from datetime import date

User = get_user_model()


class UserTests(APITestCase):

    def test_create_user(self):
        url = reverse('create-user')
        data = {
            'email': 'test@example.com',
            'password': 'passw0rd123',
            'username': 'testuser',
            'birthdate': '2000-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_create_user_invalid_data(self):
        url = reverse('create-user')
        data = {
            'email': 'invalid-email',
            'password': '',
            'username': '',
            'birthdate': '2020-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_under_age(self):
        url = reverse('create-user')
        data = {
            'email': 'test@example.com',
            'password': 'passw0rd123',
            'username': 'testuser',
            'birthdate': '2023-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_users(self):
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="passw0rd123",
            birthdate="2000-01-01"
        )
        self.client.force_authenticate(user=self.superuser)
        url = reverse("list-users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.create_user_url = reverse('create-user')
        self.login_url = reverse('login')

    def test_create_and_login_user(self):
        # create a user
        user_data = {
            'email': 'test@example.com',
            'password': 'passw0rd123',
            'username': 'testuser',
            'birthdate': '1990-01-01'
        }
        response = self.client.post(self.create_user_url, data=user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # login as the user
        login_data = {
            'email': 'test@example.com',
            'password': 'passw0rd123'
        }
        response = self.client.post(self.login_url, data=login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class GameTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass',
            birthdate='2000-01-01'
        )
        self.game = Game.objects.create(name='Super Mario', genre='Platformer')

        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password", birthdate="2000-01-01"
        )

    def test_create_game_list(self):
        url = reverse("create-game-list")
        self.client.force_authenticate(user=self.superuser)
        data = {"name": "Game 1", "genre": "Action"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_game_list(self):
        url = reverse('game-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Super Mario')
        self.assertEqual(response.data[0]['genre'], 'Platformer')

    def test_get_game_detail(self):
        url = reverse('game-detail', args=[self.game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Super Mario')
        self.assertEqual(response.data['genre'], 'Platformer')

    def test_create_play_session_unauthenticated(self):
        url = reverse('create-play-session')
        data = {
            'user': self.user.id,
            'game': self.game.id,
            'timestamp': date.today().isoformat()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_play_session_authenticated(self):
        url = reverse('create-play-session')
        self.client.force_authenticate(user=self.user)
        data = {
            'user': self.user.id,
            'game': self.game.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlaySession.objects.count(), 1)
        self.assertEqual(PlaySession.objects.get().user, self.user)
        self.assertEqual(PlaySession.objects.get().game, self.game)

