from django.urls import path
from . import views

app_name = "studios"

urlpatterns = [
    path("<int:pk>", views.SelectStudio.as_view(), name="studio"),
    path("search/", views.SearchView.as_view(), name="search"),
]
