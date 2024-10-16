from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrDeny(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve','partial_update']:
            return request.user.is_staff or request.user == view.get_object()
        return request.user.is_staff

class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
