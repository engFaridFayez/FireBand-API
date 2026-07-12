from rest_framework import viewsets
from rest_framework import permissions
from core.models import Booking, DurationOption, EventCategory, Rule, SubCategory
from core.serialziers import BookingSerializer, BookingWriteSerializer, DurationOptionSerializer, DurationOptionWriteSerializer, EventCategorySerializer, EventCategoryWriteSerializer, RuleSerializer, RuleWriteSerializer, SubCategorySerializer, SubCategoryWriteSerializer
# Create your views here.
class EventCategoryView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = EventCategory.objects.prefetch_related(
        "subcategories__rules",
        "subcategories__duration_options"
    )
    lookup_field= "slug"

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
    lookup_field= "slug"

    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return SubCategorySerializer
        return SubCategoryWriteSerializer
class RuleView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Rule.objects.select_related("sub_category")
    
    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
            return RuleSerializer
        return RuleWriteSerializer
    

class DurationView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = DurationOption.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["list","retrieve"]:
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
