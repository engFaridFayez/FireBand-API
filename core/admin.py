from django.contrib import admin

from .models import Booking, DurationOption, EventCategory, SubCategory, Rule


class RuleInline(admin.TabularInline):
    model = Rule
    extra = 1


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubCategoryInline]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)
    inlines = [RuleInline]


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ("text", "sub_category", "order")
    list_filter = ("sub_category__category", "sub_category")
    search_fields = ("text",)
    autocomplete_fields = ("sub_category",)
    ordering = ("sub_category", "order")

@admin.register(DurationOption)
class Duration(admin.ModelAdmin):
    list_display = ("title","sub_category","minutes")
    list_filter = ("sub_category__category", "sub_category")
    search_fields = ("title",)
    autocomplete_fields = ("sub_category",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "event_date",
        "event_time",
        "category",
        "sub_category",
        "duration",
        "team_members",
    )

    list_filter = (
        "category",
        "sub_category",
        "duration",
        "event_date",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
        "location",
        "custom_sub_category",
    )

    autocomplete_fields = (
        "category",
        "sub_category",
        "duration",
    )

    date_hierarchy = "event_date"

    ordering = ("-event_date", "-event_time")