from django.contrib import admin
from django.utils.html import format_html

from .models import Show, TeamMember, GalleryImage, Reel


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "location",
        "date",
        "tag",
        "image_preview",
    )
    list_filter = ("date", "city")
    search_fields = ("title", "city", "location", "tag")
    ordering = ("date",)

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return "-"


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "role",
        "accent",
        "order",
        "image_preview",
    )
    list_editable = ("order",)
    search_fields = ("name", "role")
    ordering = ("order",)

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:50%;" />',
                obj.image.url,
            )
        return "-"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "sub_category",
        "order",
        "is_active",
        "image_preview",
        "created_at",
    )
    list_filter = ("sub_category", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "sub_category__name")
    autocomplete_fields = ("sub_category",)
    ordering = ("order", "-created_at")

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return "-"


@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "sub_category",
        "platform",
        "order",
        "is_active",
        "thumbnail_preview",
        "created_at",
    )
    list_filter = ("platform", "sub_category", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "sub_category__name")
    autocomplete_fields = ("sub_category",)
    ordering = ("order", "-created_at")

    @admin.display(description="Thumbnail")
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />',
                obj.thumbnail.url,
            )
        return "-"