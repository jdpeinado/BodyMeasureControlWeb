"""Entrymeasure permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsEntryMeasureCreatror(BasePermission):
    """Allow access only to user owner."""

    def has_object_permission(self, request, view, obj):
        """Verify user is an owner of the obj."""
        return obj.user == request.user
