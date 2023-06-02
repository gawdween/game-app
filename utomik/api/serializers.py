from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from datetime import date

from .models import Game, PlaySession

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'birthdate']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'birthdate']

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate_birthdate(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("You must be 18 years or older to register")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if not email:
            raise serializers.ValidationError('Email address is required')
        if not password:
            raise serializers.ValidationError('Password is required')

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError('Invalid email or password')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')
        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': {
                'access': user.token,
                'refresh': user.refresh_token
            }
        }


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "birthdate", "is_active"]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'genre']


class PlaySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaySession
        fields = ['id', 'user', 'game', 'created_at']
        read_only_fields = ['user']
