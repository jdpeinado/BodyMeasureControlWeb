""" User admin classes"""

# Django
from django.contrib import admin

# Models
from users.models import Profile

admin.site.register(Profile)
