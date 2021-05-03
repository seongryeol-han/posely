from django.urls import path
from . import views

app_name = "concepts"

urlpatterns = [
    path("<int:pk>", views.ConceptDetail.as_view(), name="concept"),
]