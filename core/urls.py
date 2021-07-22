from django.urls import path
from studios import views as studio_view

app_name = "core"

urlpatterns = [
    # path("", studio_view.HomeView.as_view(), name="home"),
    path("", studio_view.HomeView2.as_view(), name="home"),
    path("distance/", studio_view.HomeView3.as_view(), name="home_sorted_distance"),
]
