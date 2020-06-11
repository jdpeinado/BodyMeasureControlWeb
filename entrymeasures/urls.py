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
        view=views.EntryMeasureDetailView.as_view(),
        name='detail'
    ),

    path(
        route='new/',
        view=views.CreatePostView.as_view(),
        name='create'
    ),

]