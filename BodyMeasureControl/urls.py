"""BodyMeasureControl URL Configuration"""

# Django
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        '',
        include(
            ('entrymeasures.urls', 'entrymeasures'),
            namespace='entrymeasures'
        )
    ),

    path(
        '',
        include(
            ('users.urls', 'users'),
            namespace='users'
        )
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
