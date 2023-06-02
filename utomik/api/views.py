from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser, Game, PlaySession
from .serializers import RegisterSerializer, UserListSerializer, GameSerializer, PlaySessionSerializer


class RegisterView(generics.GenericAPIView):
    """
        An endpoint to create a new user.
        """
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = serializer.data
        refresh = RefreshToken.for_user(user)
        response_data = {
            'user_info': user_data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
        An endpoint for users to login.
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(user)
        refresh = RefreshToken.for_user(user)
        response_data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        response_data.update({"user_info": serializer.data})
        return Response(response_data, status=status.HTTP_200_OK)


class UsersListView(generics.ListAPIView):
    """
        An endpoint for Staff to retrieve lists of all users.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]


class CreateGameListView(generics.CreateAPIView):
    """
    An endpoint for Staff to create new games.
    """
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAdminUser]


class GameListAPIView(generics.ListAPIView):
    """
    An endpoint that returns a list of all games.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (AllowAny,)


class GameDetailAPIView(generics.RetrieveAPIView):
    """
    An endpoint that returns the details of a specific game.
     """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (AllowAny,)


class PlaySessionCreateAPIView(generics.CreateAPIView):
    """
    An endpoint that allows a registered user to create a new play session.
    """
    serializer_class = PlaySessionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

