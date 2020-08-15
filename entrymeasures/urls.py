"""EntryMeasures URLs."""

# Django
from django.urls import path, include

# Django REST framework
from rest_framework.routers import DefaultRouter

# Views
from entrymeasures import views

router = DefaultRouter()
router.register(
    r'entrymeasures',
    views.EntryMeasureViewSet,
    basename='entrymeasure'
)

urlpatterns = [

    path('', include(router.urls)),

]
