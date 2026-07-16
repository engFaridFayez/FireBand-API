from rest_framework import serializers
from urllib.parse import urlparse
from core.models import SubCategory
from core.serialziers import SubCategorySerializer
from homeContent.models import GalleryImage, Reel, Show, TeamMember




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
    class Meta:
        model = Reel
        fields = [
            "sub_category",
            "title",
            "thumbnail",
            "platform",
            "url",
            "order",
            "is_active",
        ]

    def validate(self, attrs):
        platform = attrs.get("platform")
        url = attrs.get("url")

        if not url:
            return attrs

        domain = urlparse(url).netloc.lower()

        platform_domains = {
            "youtube": [
                "youtube.com",
                "www.youtube.com",
                "youtu.be",
            ],
            "instagram": [
                "instagram.com",
                "www.instagram.com",
            ],
            "facebook": [
                "facebook.com",
                "www.facebook.com",
                "fb.watch",
            ],
            "tiktok": [
                "tiktok.com",
                "www.tiktok.com",
                "vm.tiktok.com",
            ],
        }

        allowed_domains = platform_domains.get(platform, [])

        if not any(
            domain == allowed or domain.endswith(f".{allowed}")
            for allowed in allowed_domains
        ):
            raise serializers.ValidationError(
                {
                    "url": f"This URL does not belong to {platform.title()}."
                }
            )

        return attrs