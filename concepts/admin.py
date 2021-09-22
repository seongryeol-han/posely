from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


class PhotoInline(admin.TabularInline):
    model = models.Photo
    raw_id_fields = ("studio",)  # inline에 검색기능.


@admin.register(models.Concept)
class ConceptAdmin(admin.ModelAdmin):

    """Concept Admin Definition"""

    inlines = (PhotoInline,)

    # 이렇게 해줘야, concept에 있는 studio--> name으로 간다. 그 이유는 foreign-key 때문. search_fields할때.
    def studio_name(self, obj):
        return obj.studio.name

    list_display = (
        "name",
        "studio",
    )
    raw_id_fields = ("studio",)

    search_fields = ("studio__name",)


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = (
        "concept",
        "button_filter",
        "studio",
        "get_thumbnail",
        "random_int",
    )

    raw_id_fields = ("studio",)
    search_fields = ("studio__name",)

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"
