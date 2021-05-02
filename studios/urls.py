from django.urls import path
from . import views
from concepts import views as concept_views

app_name = "studios"

urlpatterns = [
    path("<int:pk>", concept_views.SelectConcept.as_view(), name="concept"),
    path("search/", views.SearchView.as_view(), name="search"),
]