from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission

from user_app.models import Professional

class IsOwnerOrReadOnly(IsAuthenticated):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `user`.
        return obj.user == request.user


class ProfessionalOnly(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if Professional.objects.filter(id=request.user.id):
            return True
        return False
