from django.urls import path
from studios import views as studio_view
from concepts import views as concept_view

app_name = "core"

urlpatterns = [
    # path("", studio_view.HomeView.as_view(), name="home"),
    # path("yet", studio_view.HomeView2.as_view(), name="home"),
    path("", concept_view.PhotoHomeView.as_view(), name="photo_home"),
    path("filter/", concept_view.ButtonFilterView.as_view(), name="photo_filter"),
    path(
        "photo/distance/",
        studio_view.HomeView4.as_view(),
        name="photo_home_sorted_distance",
    ),
    path("distance/", studio_view.HomeView3.as_view(), name="home_sorted_distance"),
]
