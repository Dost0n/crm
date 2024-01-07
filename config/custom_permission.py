from rest_framework import permissions


class UserCheckAdmin(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH", "DELETE", "POST")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.user_role !='user':
                return True
        
        if request.method not in self.edit_methods:
            return True

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True

    #     if request.method in permissions.SAFE_METHODS:
    #         return True

    #     if obj.user == request.user:
    #         return True
        
    #     if request.method not in self.edit_methods:
    #         return True

    #     if request.user.is_staff and request.method not in self.edit_methods:
    #         return True

    #     return False