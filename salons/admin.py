from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.

@admin.register(models.SalonBadge)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""


class ConceptInline(admin.TabularInline):
    model = models.Concept

class PhotoInline(admin.TabularInline):
    model = models.Photo
    raw_id_fields = ("salon",)  # inline에 검색기능.

class PriceListInline(admin.TabularInline):
    model = models.PriceList


@admin.register(models.Salon)
class SalonAdmin(admin.ModelAdmin):
    """Salon Admin Definition"""

    inlines = (PriceListInline,ConceptInline,)

    list_display = (
        "name",
        "location",
        "location_dong",
        "phone_number",
        "address",
        "stylist",
        "count_concepts",
    )

    def count_concepts(self, obj):
        return obj.concepts.count()  # salon에 연결된 concept 개수.

    raw_id_fields = ("stylist",)
    search_fields = ("name",)


@admin.register(models.Concept)
class ConceptAdmin(admin.ModelAdmin):

    """Concept Admin Definition"""
    inlines = (PhotoInline,)

    # 이렇게 해줘야, concept에 있는 studio--> name으로 간다. 그 이유는 foreign-key 때문. search_fields할때.
    def salon_name(self, obj):
        return obj.salon.name

    list_display = (
        "name",
        "salon",
    )
    raw_id_fields = ("salon",)

    search_fields = ("salon__name",)




@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = (
        "concept",
        "button_filter",
        "salon",
        "get_thumbnail",
        "random_int",
    )

    raw_id_fields = ("salon",)
    search_fields = ("salon__name",)

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"


@admin.register(models.PriceList)
class PriceListAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = (
        "salon",
        "get_thumbnail",
    )

    raw_id_fields = ("salon",)
    search_fields = ("salon__name",)

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"