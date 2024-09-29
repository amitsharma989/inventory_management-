from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user is None or not user.check_password(password):
                raise serializers.ValidationError(_('Invalid username or password'))

        else:
            raise serializers.ValidationError(_('Must include "username" and "password"'))

        attrs['user'] = user
        return attrs

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
