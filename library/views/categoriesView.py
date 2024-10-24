from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from library.models import Category
from library.pagination.categoriesPagination import CategoriesPagination
from library.permissions.categoriesPermission import IsStaffOrDeny, IsStaff
from library.serializers.categoriesSerializer import categoriesSerializer

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = categoriesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'description','is_active']
    pagination_class = CategoriesPagination


    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes.append(IsStaffOrDeny)
        else:
            self.permission_classes.append(IsStaff)
        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
