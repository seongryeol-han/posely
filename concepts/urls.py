from django.urls import path
from . import views

app_name = "concepts"

urlpatterns = [
    path("<int:pk>", views.ConceptDetail.as_view(), name="concept"),
    path("edit-list", views.ConceptEditListView.as_view(), name="edit-list"),
    path("<int:pk>/edit/", views.EditConceptView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.ConceptPhotosView.as_view(), name="photos"),
    path(
        "<int:concept_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
]
