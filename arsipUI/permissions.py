from rest_framework import permissions


class IsContributorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user making the request is the contributor of the media item
        return (
            request.user
            and request.user.is_authenticated
            and request.user.userprofile.user_type == "contributor"
        )
