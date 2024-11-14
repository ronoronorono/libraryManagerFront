from django.urls import path,include
from rest_framework.routers import DefaultRouter

#from .views import CategoriesViewSet

app_name = 'library'

router = DefaultRouter(
    trailing_slash=True
)

#router.register(r'categories', CategoriesViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]