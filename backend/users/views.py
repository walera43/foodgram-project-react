from rest_framework import permissions
from djoser.permissions import CurrentUserOrAdminOrReadOnly
from djoser.views import UserViewSet as CustomViewSet
from .serializers import UserCreateSerializer

from .models import User


class UserViewSet(CustomViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [CurrentUserOrAdminOrReadOnly,]

    def get_queryset(self):
        return User.objects.all()