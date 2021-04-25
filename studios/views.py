from django.views.generic import ListView
from . import models

# Create your views here.


class HomeView(ListView):
    """StudioView Definition"""

    model = models.Studio
    paginate_by = 10
    ordering = "created"
    context_object_name = "studios"