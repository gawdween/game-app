from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView, LoginView, UsersListView,
                    GameListAPIView, GameDetailAPIView, PlaySessionCreateAPIView, CreateGameListView)

urlpatterns = [
    path('users', RegisterView.as_view(), name='create-user'),
    path('login', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UsersListView.as_view(), name='list-users'),
    path('create-games/', CreateGameListView.as_view(), name='create-game-list'),
    path('games/', GameListAPIView.as_view(), name='game-list'),
    path('games/<int:pk>', GameDetailAPIView.as_view(), name='game-detail'),
    path('playsessions', PlaySessionCreateAPIView.as_view(), name='create-play-session'),
]
