from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.users.serializers import CustomUserSerializer, FollowSerializer
from users.models import CustomUser, Follow


class CustomUserViewsSet(UserViewSet):
    """отбражение пользателя"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class FollowListView(ListAPIView):
    """на кого подписан пользователь"""
    serializer_class = FollowSerializer

    def get_queryset(self):
        # return self.request.user.following.all()
        return CustomUser.objects.filter(
            following__user=self.request.user
        )


class FollowViewSet(APIView):
    """
    подписка на автора с удалением и валидацией.
    """
    serializer_class = FollowSerializer

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'error': 'вы уже подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(CustomUser, id=user_id)
        Follow.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(CustomUser, id=user_id)
        subscription = Follow.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )
