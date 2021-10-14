from django.urls import path
from . import views

app_name = "salons"

urlpatterns = [
    #salon
    path("", views.SalonHomeView.as_view(), name="salon_home"),
    path("search/", views.SalonSearchView.as_view(), name="salon_search"),
    #path("filter/", concept_view.ButtonFilterView.as_view(), name="photo_filter"),
    #path("like/", views.studio_like, name="studio_like"),  
    # 좋아요 누를시 통신하는 url 따로 페이지가 뜨는 것은 아닙니다.
    
    path("<int:pk>/", views.SalonProfileView.as_view(), name="profile"),
    path("<int:pk>/edit/", views.EditSalonView.as_view(), name="edit"),
    path("create/", views.CreateSalonView.as_view(), name="create"),
    path("<int:pk>/concept-create/", views.CreateConceptView.as_view(), name="concept-create"),
    path("distance/", views.SalonDistanceView.as_view(), name="salon_sorted_distance",),

    #concept
    path("concept/<int:pk>", views.ConceptDetail.as_view(), name="concept_detail"),
    path("concept/edit-list", views.ConceptEditListView.as_view(), name="concept_edit-list"),
    path("concept/<int:pk>/edit/", views.EditConceptView.as_view(), name="concept_edit"),
    path("concept/<int:pk>/photos/", views.ConceptPhotosView.as_view(), name="concept_photos"),
    path("concept/<int:pk>/photos/add", views.AddPhotoView.as_view(), name="concept_add-photo"),
    path("concept/<int:concept_pk>/photos/<int:photo_pk>/delete/", views.delete_photo, name="concept_delete-photo"),
    path("concept/<int:concept_pk>/delete/", views.delete_concept, name="concept_delete-concept"),

]
