from django.contrib import admin
from . import models
from concepts import models as concept_models

# Register your models here.


@admin.register(models.StudioBadge)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    pass


class ConceptInline(admin.TabularInline):
    model = concept_models.Concept


@admin.register(models.Studio)
class StudioAdmin(admin.ModelAdmin):
    """Studio Admin Definition"""

    inlines = (ConceptInline,)

    list_display = (
        "name",
        "studio_lat",
        "studio_lng",
        "phone_number",
        "kakao_chat",
        "address",
        "open_time",
        "close_time",
        "introduction",
        "using_info",
        "studio_avatar",
        "author",
        "count_concepts",
    )

    def count_concepts(self, obj):
        return obj.concepts.count()  # studio에 연결된 concept 개수.

    raw_id_fields = ("author",)
    search_fields = ("name",)
