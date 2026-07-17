from rest_framework import serializers
from urllib.parse import urlparse
from core.models import SubCategory
from core.serialziers import SubCategorySerializer
from homeContent.models import GalleryImage, Reel, Show, TeamMember
from urllib.parse import urlparse
from .utils import (
    get_facebook_embed_url,
    get_youtube_embed_url,
)


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


# Images
class GalleryImageSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(read_only=True)

    class Meta:
        model = GalleryImage
        fields = "__all__"

class GalleryImageWriteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    class Meta:
        model = GalleryImage
        fields = [
            "sub_category",
            "image",
            "title",
            "order",
            "is_active",
        ]
class GalleryBulkUploadSerializer(serializers.Serializer):
    sub_category = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all()
    )

    images = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty=False,
    )

    title = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    is_active = serializers.BooleanField(default=True)


#Reels
class ReelSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(read_only=True)
    platform_display = serializers.CharField(
        source="get_platform_display",
        read_only=True,
    )

    class Meta:
        model = Reel
        fields = "__all__"


class ReelWriteSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Reel
        fields = [
            "sub_category",
            "title",
            "thumbnail",
            "platform",
            "embed_url",
            "order",
            "is_active",
        ]

    def validate(self, attrs):
        platform = attrs.get("platform")
        url = attrs.get("embed_url")

        if not url:
            return attrs

        domain = urlparse(url).netloc.lower()

        platform_domains = {
            "youtube": [
                "youtube.com",
                "www.youtube.com",
                "youtu.be",
            ],
            "facebook": [
                "facebook.com",
                "www.facebook.com",
                "fb.watch",
            ],
        }

        allowed_domains = platform_domains.get(platform, [])

        if not any(
            domain == allowed or domain.endswith(f".{allowed}")
            for allowed in allowed_domains
        ):
            raise serializers.ValidationError(
                {
                    "embed_url": f"This URL does not belong to {platform.title()}."
                }
            )

        converters = {
            "youtube": get_youtube_embed_url,
            "facebook": get_facebook_embed_url,
        }

        attrs["embed_url"] = converters[platform](url)

        return attrs