from django.db import models
from core import models as core_models

# Create your models here.


class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition"""

    caption = models.CharField(max_length=80, default="")
    file = models.ImageField(upload_to="concept_photos")  # /uploads/concept_photos에 저장.
    concept = models.ForeignKey(
        "Concept", related_name="photos", on_delete=models.CASCADE
    )
    studio = models.ForeignKey(
        "studios.Studio",
        related_name="photos",
        on_delete=models.CASCADE,
        default=False,
    )

    def __str__(self):
        return self.caption


class Concept(core_models.TimeStampedModel):
    """Concept Model Definition"""

    name = models.CharField(max_length=30)
    concept_description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    service_config = models.TextField()
    studio = models.ForeignKey(
        "studios.Studio",
        related_name="concepts",  # studio에서 concept을 "concepts"으로 사용하면 된다.
        on_delete=models.CASCADE,
        default=False,
    )

    def __str__(self):
        return self.name
