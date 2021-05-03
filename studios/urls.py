from django.urls import path
from . import views
from studios import views as studios_views

app_name = "studios"

urlpatterns = [
    path("<int:potato>", studios_views.SelectStudio.as_view(), name="studio"),
    path("search/", views.SearchView.as_view(), name="search"),
]