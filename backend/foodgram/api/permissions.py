from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin
                         or request.user.is_superuser)))


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.author
                or request.user.is_moderator
                or request.user.is_admin
                or request.user.is_superuser)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous and (
            request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return not request.user.is_anonymous and (
            request.user.is_admin
            or request.user.is_superuser
        )
