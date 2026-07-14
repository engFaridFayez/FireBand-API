from rest_framework import serializers
from datetime import date
from core.models import Booking, DurationOption, EventCategory, Rule, SubCategory


#=======================================
#               GET 
#=======================================
class RuleSerializer(serializers.ModelSerializer):
    sub_category_name = serializers.CharField(
        source="sub_category.name",
        read_only=True,
    )

    class Meta:
        model = Rule
        fields = [
            "id",
            "text",
            "order",
            "sub_category",
            "sub_category_name",
        ]
class DurationOptionSerializer(serializers.ModelSerializer):
    sub_category_name = serializers.CharField(
        source="sub_category.name",
        read_only=True,
    )

    class Meta:
        model = DurationOption
        fields = [
            "id",
            "title",
            "minutes",
            "sub_category",
            "sub_category_name",
        ]
class SubCategorySerializer(serializers.ModelSerializer):
    rules = RuleSerializer(many=True,read_only=True)
    duration = DurationOptionSerializer(source="duration_options",many=True,read_only=True)
    class Meta:
        model = SubCategory
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'image',
            "category",
            'duration',
            'rules',
            "min_members",
            "max_members"
        ]
class EventCategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True,read_only=True)
    class Meta:
        model = EventCategory
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'description',
            'subcategories'
        ]


class BookingSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(read_only=True)
    sub_category = SubCategorySerializer(read_only=True)
    duration = DurationOptionSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"


#=======================================
#         POST , PUT , PATCH
#=======================================

class EventCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = [
            "name",
            "image",
            "description",
        ]
class SubCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            "name",
            "image",
            "description",
            "category",
            "min_members",
            "max_members"
        ]
class RuleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = "__all__"
class DurationOptionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DurationOption
        fields = "__all__"

class BookingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "event_date",
            "event_time",
            "location",
            "category",
            "sub_category",
            "custom_sub_category",
            "duration",
            "team_members",
            "notes",
        ]

    def validate(self,attrs):
        category = attrs.get("category", self.instance.category if self.instance else None)
        sub_category = attrs.get("sub_category", self.instance.sub_category if self.instance else None)
        duration = attrs.get("duration", self.instance.duration if self.instance else None)
        members = attrs.get("team_members", self.instance.team_members if self.instance else None)

        if sub_category.category != category:
            raise serializers.ValidationError({
                "sub_category": "Sub category doesn't belong to the selected category"
            })
        
        if duration.sub_category != sub_category:
            raise serializers.ValidationError({
                "duration": "Duration doesn't belong to the selected sub category."
            })

        if members < sub_category.min_members or members > sub_category.max_members:
            raise serializers.ValidationError({
                "team_members":
                    f"Members must be between {sub_category.min_members} and {sub_category.max_members}."
            })
        
        if sub_category.slug == "other" and not attrs.get("custom_sub_category"):
            raise serializers.ValidationError({
                "custom_sub_category": "This field is required."
            })
        
        if sub_category.slug != "other" and attrs.get("custom_sub_category"):
            raise serializers.ValidationError({
                "custom_sub_category": "This field can only be used with the 'other' sub category."
            })
        
        if attrs.get("event_date") and attrs["event_date"] < date.today():
            raise serializers.ValidationError({
                "event_date": "Event date cannot be in the past."
            })
        
        return attrs