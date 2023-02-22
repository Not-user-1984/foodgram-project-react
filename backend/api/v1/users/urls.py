from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowListView, FollowViewSet, CustomUserViewsSet


router = DefaultRouter()
router.register('users', CustomUserViewsSet, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/',
        FollowListView.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        FollowViewSet.as_view(),
        name='subscribe'
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
