from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as CustomViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe, User
from .serializers import SubscribeSerializer, UserDetailSerializer


class UserViewSet(CustomViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()

    @action(methods=['GET', 'DELETE'], detail=True, url_path='subscribe')
    def subscribe(self, request, id):
        current_author = get_object_or_404(User, id=id)
        current_user = request.user
        if current_user == current_author:
            return Response(
                'Подписка на самого себя запрещена',
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'GET':
            obj, created = Subscribe.objects.get_or_create(
                user=current_user,
                author=current_author
            )
            if not created:
                return Response(
                    'Вы уже подписаны на этого пользователя',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = UserDetailSerializer(
                current_author,
                context={'request': request}
            )
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            get_object_or_404(
                Subscribe,
                user=current_user,
                author=current_author,
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SubscriptionsViewSet(ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
