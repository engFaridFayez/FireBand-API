from rest_framework import viewsets
from rest_framework import permissions
from core.bookings.services.email_service import send_booking_email
from core.models import Booking, DurationOption, EventCategory, Rule, SubCategory
from core.serialziers import BookingSerializer, BookingWriteSerializer, DurationOptionSerializer, DurationOptionWriteSerializer, EventCategorySerializer, EventCategoryWriteSerializer, RuleSerializer, RuleWriteSerializer, SubCategorySerializer, SubCategoryWriteSerializer
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
class EventCategoryView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = EventCategory.objects.prefetch_related(
        "subcategories__rules",
        "subcategories__duration_options"
    )

    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return EventCategorySerializer
        return EventCategoryWriteSerializer
    
class SubCategoryView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = SubCategory.objects.select_related(
        "category"
    ).prefetch_related(
        "rules",
        "duration_options"
    )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SubCategorySerializer
        return SubCategoryWriteSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get("category")
        if category_id is not None:
            qs = qs.filter(category_id=category_id)
        return qs
class RuleView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Rule.objects.select_related(
        "sub_category",
        "sub_category__category",
    )
    
    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return RuleSerializer
        return RuleWriteSerializer
    

class DurationView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = DurationOption.objects.select_related(
        "sub_category",
        "sub_category__category",
    )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return DurationOptionSerializer
        return DurationOptionWriteSerializer

class BookingView(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related(
        "category",
        "sub_category",
        "duration",
    )
    

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BookingSerializer
        return BookingWriteSerializer
    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    def perform_create(self, serializer):
        serializer.save()