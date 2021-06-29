from django.urls import path
from . import views

app_name = "studios"

urlpatterns = [
    path("<int:pk>", views.SelectStudio.as_view(), name="studio"),
    path("search/", views.SearchView.as_view(), name="search"),
    path(
        "like/", views.studio_like, name="studio_like"
    ),  # 좋아요 누를시 통신하는 url 따로 페이지가 뜨는 것은 아닙니다.
    path("<int:pk>/", views.StudioProfileView.as_view(), name="profile"),
    path("<int:pk>/edit/", views.EditStudioView.as_view(), name="edit"),
    path("create/", views.CreateStudioView.as_view(), name="create"),
]
