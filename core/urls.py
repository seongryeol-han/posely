from django.urls import path
from studios import views as studio_view
from concepts import views as concept_view

app_name = "core"

urlpatterns = [
    path("", concept_view.StudioHomeView.as_view(), name="studio_home"),
]
