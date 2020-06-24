"""BodyMeasures users views"""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

# Forms
from users.forms import SignupForm, UpdateProfileForm

# Models
from users.models import Profile

# Utils
from measurement.measures import Distance


class UpdateProfileView(FormView):
    """Update profile view"""

    template_name = 'users/update_profile.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('users:update')

    def form_valid(self, form):
        """Save form data."""
        form.save(self.request.user.profile)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        profile = self.request.user.profile
        if profile.measurement_system == 'METRIC':
            profile.height = Distance(m=profile.height.m)
        context['profile'] = profile
        return context

class SignupView(FormView):
    """Users sign up view."""

    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)

class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'users/login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = ''
