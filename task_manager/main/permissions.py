from rest_framework import permissions


class DeleteOnlyForStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            return request.user.is_staff
        return True
