"""EntryMeasures views."""

# Django REST framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Permissions
from entrymeasures.permissions import IsEntryMeasureCreatror

# Serializer
from entrymeasures.serializers import (
    EntryMeasureModelSerializer,
    EntryMeasureCreateModelSerializer
)

# Filters
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Models
from entrymeasures.models import EntryMeasure


class EntryMeasureViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """EntryMeasure view set."""

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    lookup_field = 'date_measure'
    ordering = ('-date_measure')

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = EntryMeasure.objects.filter(active=True)
        if self.action in ['list', 'retrieve', 'put', 'patch']:
            return queryset.filter(user=self.request.user)
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'delete']:
            permissions.append(IsEntryMeasureCreatror)
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """Get correct serializer for create action."""
        if self.action in ['create']:
            return EntryMeasureCreateModelSerializer
        else:
            return EntryMeasureModelSerializer

    def perform_destroy(self, instance):
        """Do not delete the object, just change active to False."""
        instance.active = False
        instance.save()
