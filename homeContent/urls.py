from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    GalleryImageViewSet,
    ReelViewSet,
    ShowViewset,
    TeamViewset
)

router = DefaultRouter()

router.register(r'shows', ShowViewset,basename='shows')
router.register(r'team',TeamViewset,basename='team')
router.register(r"gallery", GalleryImageViewSet, basename="gallery")
router.register(r"reels", ReelViewSet, basename="reel")



urlpatterns = [
    path('', include(router.urls)),
]