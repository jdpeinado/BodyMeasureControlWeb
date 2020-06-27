"""EntryMeasures URLs."""

# Django
from django.urls import path

# Views
from entrymeasures import views

urlpatterns = [

    path(
        route='',
        view=views.EntryMeasuresView.as_view(),
        name='list'
    ),

    path(
        route='<int:pk>/',
        view=views.UpdateEntryMeasureView.as_view(),
        name='edit'
    ),

    path(
        route='detail/<int:pk>/',
        view=views.DetailEntryMeasureView.as_view(),
        name='detail'
    ),

    path(
        route='add/',
        view=views.AddEntryMeasureView.as_view(),
        name='create'
    ),

]