"""EntryMeasures views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

# Models
from entrymeasures.models import EntryMeasure

# Forms
from entrymeasures.forms import EntryMeasureForm


class EntryMeasuresView(LoginRequiredMixin, ListView):
    """Return all entrymeasures."""

    template_name = 'entrymeasures/list_measures.html'
    model = EntryMeasure
    ordering = ('-created_at',)
    paginate_by = 30
    context_object_name = 'entrymeasures'

class EntryMeasureDetailView(LoginRequiredMixin, DetailView):
    """Return entry measure detail."""

    template_name = 'entrymeasures/detail.html'
    queryset = EntryMeasure.objects.all()
    context_object_name = 'entrymeasure'

class CreatePostView(LoginRequiredMixin, CreateView):
    """Create a new post."""

    template_name = 'entrymeasures/new.html'
    form_class = EntryMeasureForm
    success_url = reverse_lazy('entrymeasures:list')

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context

