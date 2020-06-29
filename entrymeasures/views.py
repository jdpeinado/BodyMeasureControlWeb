"""EntryMeasures views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.paginator import Paginator

# Models
from entrymeasures.models import EntryMeasure

# Forms
from entrymeasures.forms import EntryMeasureForm, UpdateEntryMeasureForm, CompareEntryMeasureForm
from django.views.generic import FormView

# Utils
from measurement.measures import Distance, Weight
import copy
from datetime import datetime


class EntryMeasuresView(LoginRequiredMixin, ListView):
    """Return all entrymeasures."""

    template_name = 'entrymeasures/list_measures.html'
    model = EntryMeasure
    ordering = ('-date_measure',)
    paginate_by = 10
    context_object_name = 'entrymeasures'

    def get(self, request, *args, **kwargs):
        queryset, date = self.get_queryset() 
        if queryset.count() == 1 and date:
            return redirect('entrymeasures:detail', pk=queryset.first().pk)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        date = self.request.GET.get('date_measure',None)
        if date:
            entrymeasure = EntryMeasure.objects.filter(date_measure=date,active=True, user=self.request.user)
            self.search = "Any measure found for the selected date"
        else:
            entrymeasure = EntryMeasure.objects.filter(user=self.request.user,active=True).order_by('-date_measure')
        return entrymeasure, date

    def get_context_data(self,**kwargs):
        """ Add differences between entrymeasures"""

        context = super(EntryMeasuresView,self).get_context_data(**kwargs)

        entrymeasures = EntryMeasure.objects.filter(user=self.request.user,active=True).order_by('-date_measure')
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
        if hasattr(self,'search'):
            context['search'] = self.search

        return context

class CompareEntryMeasureView(FormView):

    template_name = 'entrymeasures/compare.html'

    def get(self, request, *args, **kwargs):
        form = CompareEntryMeasureForm()
        self.entrymeasure1 = None
        self.entrymeasure2 = None
        self.entrymeasure_resume = None
        form = CompareEntryMeasureForm(self.request.GET or None, request=request)
        if form.is_valid():
            self.test = 'this is a test with vars from get'
            date_measure1 = form.cleaned_data['date_measure1']
            date_measure2 = form.cleaned_data['date_measure2']
            entry_measure1 = EntryMeasure.objects.filter(active=True, user=self.request.user, date_measure=date_measure1)
            entry_measure2 = EntryMeasure.objects.filter(active=True, user=self.request.user, date_measure=date_measure2)
            if entry_measure1.count()==1 and entry_measure2.count()==1:
                entry_measure1 = entry_measure1.first()
                entry_measure1.change_units(self.request.user.profile.measurement_system)
                entry_measure2 = entry_measure2.first()
                entry_measure2.change_units(self.request.user.profile.measurement_system)

                if entry_measure1.date_measure>=entry_measure2.date_measure:
                    self.entrymeasure_resume = copy.copy(entry_measure1)
                    to_diff = entry_measure2
                else:
                    self.entrymeasure_resume = copy.copy(entry_measure2)
                    to_diff = entry_measure1

                self.entrymeasure_resume.change_units(self.request.user.profile.measurement_system)
                self.entrymeasure_resume.bodyweight_diff = self.entrymeasure_resume.bodyweight - to_diff.bodyweight
                self.entrymeasure_resume.chest_diff = self.entrymeasure_resume.chest - to_diff.chest
                self.entrymeasure_resume.waist_diff = self.entrymeasure_resume.waist - to_diff.waist
                self.entrymeasure_resume.hip_diff = self.entrymeasure_resume.hip - to_diff.hip
                self.entrymeasure_resume.leg_diff = self.entrymeasure_resume.leg - to_diff.leg
                self.entrymeasure_resume.bicep_diff = self.entrymeasure_resume.bicep - to_diff.bicep

                self.entrymeasure1 = entry_measure1
                self.entrymeasure2 = entry_measure2

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(CompareEntryMeasureView, self).get_context_data(**kwargs)
        context.update({
            'entrymeasure1': self.entrymeasure1,
            'entrymeasure2': self.entrymeasure2,
            'entrymeasure_resume': self.entrymeasure_resume,
        })
        return context
    

class DetailEntryMeasureView(LoginRequiredMixin, DetailView):
    """Detail entry measure"""
    template_name = 'entrymeasures/detail_entrymeasure.html'

    def get_queryset(self):
        return EntryMeasure.objects.filter(active=True, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['entrymeasure'].change_units(self.request.user.profile.measurement_system)
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

