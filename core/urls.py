from django.urls import path
from studios import views as studio_view
from concepts import views as concept_view

app_name = "core"

urlpatterns = [
    # path("", studio_view.HomeView.as_view(), name="home"),
    path("", studio_view.HomeView2.as_view(), name="home"),
    path("photo", concept_view.PhotoHomeView.as_view(), name="photo_home"),
    path("distance/", studio_view.HomeView3.as_view(), name="home_sorted_distance"),
]
