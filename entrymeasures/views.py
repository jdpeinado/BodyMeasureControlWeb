"""EntryMeasures views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import FormView

# Models
from entrymeasures.models import EntryMeasure

# Forms
from entrymeasures.forms import EntryMeasureForm, UpdateEntryMeasureForm

# Utils
from measurement.measures import Distance, Weight
import copy


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

            pos = i+1
            if (i+1)==len(entrymeasures):
                pos = i

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
            entrymeasure_resume = copy.copy(entrymeasures[0])
            entrymeasure_resume.change_units(self.request.user.profile.measurement_system)
            entrymeasure_resume.bodyweight_diff = entrymeasure_resume.bodyweight - entrymeasures.last().bodyweight
            entrymeasure_resume.chest_diff = entrymeasure_resume.chest - entrymeasures.last().chest
            entrymeasure_resume.waist_diff = entrymeasure_resume.waist - entrymeasures.last().waist
            entrymeasure_resume.hip_diff = entrymeasure_resume.hip - entrymeasures.last().hip
            entrymeasure_resume.leg_diff = entrymeasure_resume.leg - entrymeasures.last().leg
            entrymeasure_resume.bicep_diff = entrymeasure_resume.bicep - entrymeasures.last().bicep
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

class UpdateEntryMeasureView(LoginRequiredMixin, UpdateView):
    """Update entry measure."""

    template_name = 'entrymeasures/update_entrymeasure.html'
    model = EntryMeasure
    form_class = UpdateEntryMeasureForm
    success_url = reverse_lazy('entrymeasures:list')

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['entrymeasure'].change_units(self.request.user.profile.measurement_system)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context


class AddEntryMeasureView(LoginRequiredMixin, CreateView):
    """Add a new measure."""

    template_name = 'entrymeasures/add.html'
    form_class = EntryMeasureForm
    success_url = reverse_lazy('entrymeasures:list')

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context

