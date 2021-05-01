from django.urls import path
from . import views

app_name = "studios"

urlpatterns = [
    path("search/", views.SearchView.as_view(), name="search"),
]