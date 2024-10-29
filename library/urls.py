from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import CustomUserProfileViewSet, CategoriesViewSet, PublisherViewSet, AuthorViewSet

app_name = 'library'

router = DefaultRouter(
    trailing_slash=True
)

router.register(r'users', CustomUserProfileViewSet, basename='customuserprofile')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'publishers', PublisherViewSet, basename='publishers')
router.register(r'authors', AuthorViewSet, basename='authors')

urlpatterns = [
    path('', include(router.urls)),
]