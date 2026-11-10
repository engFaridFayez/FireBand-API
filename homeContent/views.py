from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsAdminOrReadOnly
from homeContent.models import GalleryImage, Reel, Show, TeamMember
from homeContent.serialziers import GalleryBulkUploadSerializer, GalleryImageSerializer, GalleryImageWriteSerializer, ReelSerializer, ReelWriteSerializer, ShowSerializer, TeamSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Max
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from xml.etree import ElementTree as ET
from urllib.parse import quote
from django.conf import settings
# Create your views here.

@require_GET
def sitemap_xml(request):
    base_url = settings.PUBLIC_SITE_URL.rstrip("/")

    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)

    root = ET.Element(f"{{{namespace}}}urlset")

    def add_url(url):
        url_element = ET.SubElement(
            root,
            f"{{{namespace}}}url"
        )

        ET.SubElement(
            url_element,
            f"{{{namespace}}}loc"
        ).text = url

    # Static public pages
    add_url(f"{base_url}/")
    add_url(f"{base_url}/portfolio")
    add_url(f"{base_url}/pricing")

    # Dynamic active reels
    slugs = Reel.objects.filter(
        is_active=True
    ).exclude(
        slug=""
    ).values_list("slug", flat=True)

    for slug in slugs:
        encoded_slug = quote(slug, safe="")
        add_url(f"{base_url}/videos/{encoded_slug}")

    xml_content = ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )

    return HttpResponse(
        xml_content,
        content_type="application/xml; charset=utf-8"
    )
class ShowViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class TeamViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = TeamMember.objects.all()
    serializer_class = TeamSerializer

class GalleryImagePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 60

class GalleryImageViewSet(viewsets.ModelViewSet):
    pagination_class = GalleryImagePagination
    queryset = GalleryImage.objects.select_related(
        "sub_category",
        "sub_category__category",
    )

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return GalleryImageWriteSerializer
        return GalleryImageSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [IsAdminOrReadOnly()]

    def get_queryset(self):
        queryset = super().get_queryset()

        subcategory = self.request.query_params.get("subcategory")
        active = self.request.query_params.get("active")

        if subcategory:
            queryset = queryset.filter(sub_category_id=subcategory)

        # المستخدم العادي يشوف الصور المفعلة فقط
        if self.request.user.is_staff:
            if active is not None:
                queryset = queryset.filter(
                    is_active=active.lower() == "true"
                )
        else:
            queryset = queryset.filter(is_active=True)

        return queryset

    @action(detail=False,methods=["post"],permission_classes=[IsAdminOrReadOnly],)
    def bulk(self, request):
        serializer = GalleryBulkUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sub_category = serializer.validated_data["sub_category"]
        images = serializer.validated_data["images"]
        title = serializer.validated_data.get("title", "")
        is_active = serializer.validated_data["is_active"]

        last_order = (
            GalleryImage.objects.filter(sub_category=sub_category)
            .aggregate(Max("order"))["order__max"]
            or 0
        )

        created = []

        with transaction.atomic():
            for index, image in enumerate(images):
                created.append(
                    GalleryImage.objects.create(
                        sub_category=sub_category,
                        image=image,
                        title=title,
                        order=last_order + index + 1,
                        is_active=is_active,
                    )
                )

        return Response(
            {
                "message": "Images uploaded successfully.",
                "count": len(created),
                "results": GalleryImageSerializer(created, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ReelViewSet(viewsets.ModelViewSet):
    queryset = Reel.objects.select_related(
        "sub_category",
        "sub_category__category",
    )

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ReelWriteSerializer
        return ReelSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "by_slug"]:
            return [permissions.AllowAny()]

        return [IsAdminOrReadOnly()]

    def get_queryset(self):
        queryset = super().get_queryset()

        subcategory = self.request.query_params.get("subcategory")
        platform = self.request.query_params.get("platform")
        active = self.request.query_params.get("active")

        if subcategory:
            queryset = queryset.filter(sub_category_id=subcategory)

        if platform:
            queryset = queryset.filter(platform=platform)

        # المستخدم العادي يشوف الريلز المفعلة فقط
        if self.request.user.is_staff:
            if active is not None:
                queryset = queryset.filter(
                    is_active=active.lower() == "true"
                )
        else:
            queryset = queryset.filter(is_active=True)

        return queryset
    
    @action(
        detail=False,
        methods=["get"],
        url_path=r"by-slug/(?P<slug>[^/.]+)"
    )
    def by_slug(self, request, slug=None):
        reel = get_object_or_404(
            Reel.objects.select_related(
                "sub_category",
                "sub_category__category"
            ),
            slug=slug,
            is_active=True
        )

        serializer = self.get_serializer(reel)

        return Response(serializer.data)
