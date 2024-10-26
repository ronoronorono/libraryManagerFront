from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from library.models import CustomUserProfile
from library.pagination.customUserProfilePagination import CustomUserProfilePagination
from library.permissions.customUserProfilePermission import IsOwnerOrStaff, IsStaffOrDeny
from library.serializers.customUserProfileSerializer import CustomUserProfileSerializer


class CustomUserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUserProfile.objects.all()
    serializer_class = CustomUserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'library_card_number', 'email', 'is_active']
    pagination_class = CustomUserProfilePagination


    def get_permissions(self):
        if self.action in ['list','create','destroy']:
            self.permission_classes.append(IsStaffOrDeny)
        else:
            self.permission_classes.append(IsOwnerOrStaff)
        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context