"""EntryMeasures views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

# Models
from entrymeasures.models import EntryMeasure

# Forms
from entrymeasures.forms import EntryMeasureForm

# Utils
from measurement.measures import Distance, Weight


class EntryMeasuresView(LoginRequiredMixin, ListView):
    """Return all entrymeasures."""

    template_name = 'entrymeasures/list_measures.html'
    model = EntryMeasure
    ordering = ('-date_measure',)
    paginate_by = 10
    context_object_name = 'entrymeasures'

    def get_context_data(self,**kwargs):
        """ Add differences between entrymeasures"""
        context = super(EntryMeasuresView,self).get_context_data(**kwargs)

        entrymeasures = EntryMeasure.objects.filter(user=self.request.user).order_by('-date_measure')
        bodyweight_arr = []
        chest_arr = []
        waist_arr = []
        hip_arr = []
        leg_arr = []
        bicep_arr = []
        for i,entrymeasure in enumerate(entrymeasures):
            entrymeasure.change_units(self.request.user.profile.measurement_system)

            pos = i-1
            if i==0:
                pos = 0

            entrymeasure.bodyweight_diff = entrymeasure.bodyweight - entrymeasures[pos].bodyweight
            entrymeasure.chest_diff = entrymeasure.chest - entrymeasures[pos].chest
            entrymeasure.waist_diff = entrymeasure.waist - entrymeasures[pos].waist
            entrymeasure.hip_diff = entrymeasure.hip - entrymeasures[pos].hip
            entrymeasure.leg_diff = entrymeasure.leg - entrymeasures[pos].leg
            entrymeasure.bicep_diff = entrymeasure.bicep - entrymeasures[pos].bicep
            
            bodyweight_arr.append(entrymeasure.bodyweight.value)
            chest_arr.append(entrymeasure.chest.value)
            waist_arr.append(entrymeasure.waist.value)
            hip_arr.append(entrymeasure.hip.value)
            leg_arr.append(entrymeasure.leg.value)
            bicep_arr.append(entrymeasure.bicep.value)

        if len(entrymeasures) > 0:
            entrymeasure_resume = entrymeasures.last()
            entrymeasure_resume.change_units(self.request.user.profile.measurement_system)
            entrymeasure_resume.bodyweight_diff = entrymeasure_resume.bodyweight - entrymeasures[0].bodyweight
            entrymeasure_resume.chest_diff = entrymeasure_resume.chest - entrymeasures[0].chest
            entrymeasure_resume.waist_diff = entrymeasure_resume.waist - entrymeasures[0].waist
            entrymeasure_resume.hip_diff = entrymeasure_resume.hip - entrymeasures[0].hip
            entrymeasure_resume.leg_diff = entrymeasure_resume.leg - entrymeasures[0].leg
            entrymeasure_resume.bicep_diff = entrymeasure_resume.bicep - entrymeasures[0].bicep
            entrymeasure_resume.imc = round(entrymeasure_resume.bodyweight.kg / (entrymeasure_resume.profile.height.m**2),2)
        else:
            entrymeasure_resume = None

        p = Paginator(entrymeasures, self.paginate_by)
        context['entrymeasures'] = p.page(context['page_obj'].number)
        context['entrymeasure_resume'] = entrymeasure_resume
        context['bodyweight_arr'] = bodyweight_arr
        context['chest_arr'] = chest_arr
        context['waist_arr'] = waist_arr
        context['hip_arr'] = hip_arr
        context['leg_arr'] = leg_arr
        context['bicep_arr'] = bicep_arr

        return context

class EntryMeasureDetailView(LoginRequiredMixin, DetailView):
    """Return entry measure detail."""

    template_name = 'entrymeasures/detail.html'
    queryset = EntryMeasure.objects.all()
    context_object_name = 'entrymeasure'

class AddEntryMeasureView(LoginRequiredMixin, CreateView):
    """Add a new measure."""

    template_name = 'entrymeasures/new.html'
    form_class = EntryMeasureForm
    success_url = reverse_lazy('entrymeasures:list')

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context

