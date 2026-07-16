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
# Create your views here.
class ShowViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class TeamViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = TeamMember.objects.all()
    serializer_class = TeamSerializer


class GalleryImageViewSet(viewsets.ModelViewSet):
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
        if self.action in ["list", "retrieve"]:
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