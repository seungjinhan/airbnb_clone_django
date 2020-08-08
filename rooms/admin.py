from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "userd_by"
    )

    def userd_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo admin """

    list_display = (
        '__str__', 'get_thumbnail'
    )

    def get_thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.file.url}" width=50 >')

    get_thumbnail.short_description = "Thumbnail"


class PhotoInline(admin.StackedInline):
    model = models.Photo


# class PhotoInline(admin.TabularInline):
#     model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country",
                        "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out")},),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules",),
            },
        ),
        ("Space", {"fields": ("guests", "beds", "bedrooms", "baths",)},),
        ("Last Details", {"fields": ("host",)},),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = (
        "name",
        "price",
        "bedrooms",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    search_fields = ("=city", "^host__username")

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # def save_model(self, request, obj, form, change):
    #     super().save_model( request, obj, form, change)

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "amenities count"

    def count_photos(self, obj):
        return obj.amenities.count()

    count_photos.short_description = "photos count"
