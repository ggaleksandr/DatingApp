from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import AppUser
from .serializers import AppUserSerializer


class AppUserCreateView(generics.CreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [AllowAny]