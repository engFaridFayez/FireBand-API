from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShowViewset,
    TeamViewset
)

router = DefaultRouter()

router.register(r'shows', ShowViewset,basename='shows')
router.register(r'team',TeamViewset,basename='team')



urlpatterns = [
    path('', include(router.urls)),
]