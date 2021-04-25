from django.urls import path
from studios import views as studio_view

app_name = "core"

urlpatterns = [path("", studio_view.HomeView.as_view(), name="home")]
