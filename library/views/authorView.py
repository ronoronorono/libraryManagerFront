from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from library.models import Author
from library.pagination.customPagination import CustomPagination
from library.permissions.customPermissions import IsStaffOrDeny, IsStaff
from library.serializers.authorSerializer import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name','is_active']
    pagination_class = CustomPagination


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