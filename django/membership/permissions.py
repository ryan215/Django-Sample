from rest_framework.permissions import IsAuthenticated


class IsAdminOrSelf(IsAuthenticated):
    """
    Allow access to admin users or the user himself.
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        elif obj.email == request.user.email:
            return True
        return False
