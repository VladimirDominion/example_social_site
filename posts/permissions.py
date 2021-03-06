from rest_framework import permissions


class PostPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return request.user == obj.author


class IsAuthor(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
