from django.urls import path
from concepts import views as concept_view
from . import views

app_name = "studios"

urlpatterns = [
    #studio
    path("search/", views.StudioSearchView.as_view(), name="studio_search"),
    path("filter/", concept_view.ButtonFilterView.as_view(), name="photo_filter"),
    path(
        "like/", views.studio_like, name="studio_like"
    ),  # 좋아요 누를시 통신하는 url 따로 페이지가 뜨는 것은 아닙니다.
    path("<int:pk>/", views.StudioProfileView.as_view(), name="profile"),
    path("<int:pk>/edit/", views.EditStudioView.as_view(), name="edit"),
    path("create/", views.CreateStudioView2.as_view(), name="create"),
    path(
        "<int:pk>/concept-create/",
        views.CreateConceptView.as_view(),
        name="concept-create",
    ),
    path(
        "distance/",
        views.StudioDistanceView.as_view(),
        name="studio_sorted_distance",
    ),

    #concept
    path("concept/<int:pk>", concept_view.ConceptDetail.as_view(), name="concept_detail"),
    path("concept/edit-list", concept_view.ConceptEditListView.as_view(), name="concept_edit-list"),
    path("concept/<int:pk>/edit/", concept_view.EditConceptView.as_view(), name="concept_edit"),
    path("concept/<int:pk>/photos/", concept_view.ConceptPhotosView.as_view(), name="concept_photos"),
    path("concept/<int:pk>/photos/add", concept_view.AddPhotoView.as_view(), name="concept_add-photo"),
    path(
        "concept/<int:concept_pk>/photos/<int:photo_pk>/delete/",
        concept_view.delete_photo,
        name="concept_delete-photo",
    ),
    path(
        "concept/<int:concept_pk>/delete/",
        concept_view.delete_concept,
        name="concept_delete-concept",
    ),

]
