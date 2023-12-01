from rest_framework import permissions


class IsContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.userprofile.user_type == "contributor"


class IsVerificator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.userprofile.user_type == "verificator"
