from django.urls import path
from . import views

app_name = "concepts"

urlpatterns = [
    path("<int:pk>", views.ConceptDetail.as_view(), name="concept"),
    path("edit-list", views.ConceptEditListView.as_view(), name="edit-list"),
]
