from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrDeny(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve','list']:
            return True
        return request.user.is_staff

class IsStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff