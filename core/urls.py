from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EventCategoryView,
    SubCategoryView,
    RuleView,
    DurationView,
    BookingView
)

router = DefaultRouter()

router.register(r'categories', EventCategoryView,basename='categories')
router.register(r'subcategories',SubCategoryView,basename='sub-categories')
router.register(r'rules',RuleView,basename='rules')
router.register(r'durations',DurationView,basename='durations')
router.register(r'bookings',BookingView,basename='bookings')



urlpatterns = [
    path('', include(router.urls)),
]